import os
import time
import argparse
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
BIGQUERY_DATASET_NAME = os.getenv("BIGQUERY_DATASET_NAME")


def generate_user_count_features(aggregation_end_date):
    table_id = f"{PROJECT_ID}.{BIGQUERY_DATASET_NAME}.user_count_transactions_7d"

    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig(destination=table_id, write_disposition='WRITE_APPEND')

    aggregation_start_date = datetime.now() - timedelta(days=7)

    sql = f"""
    SELECT
        src_account AS user_id,
        COUNT(*) AS transaction_count_7d,
        timestamp'{aggregation_end_date.isoformat()}' AS feature_timestamp
    FROM
        {PROJECT_ID}.{BIGQUERY_DATASET_NAME}.transactions
    WHERE
        timestamp BETWEEN TIMESTAMP('{aggregation_start_date.isoformat()}')
        AND TIMESTAMP('{aggregation_end_date.isoformat()}')
    GROUP BY
        user_id
    """

    query_job = client.query(sql, job_config=job_config)
    query_job.result()
    print(f"Generated features as of {aggregation_end_date.isoformat()}")


def backfill_features(earliest_aggregation_end_date, interval, num_iterations):
    aggregation_end_date = earliest_aggregation_end_date
    for _ in range(num_iterations):
        generate_user_count_features(aggregation_end_date=aggregation_end_date)
        time.sleep(1)
        aggregation_end_date += interval


def update_transactions_timestamp():
    sql = """
    SELECT *
    FROM `feast-oss.fraud_tutorial.transactions`
    """

    # Run a Standard SQL query using the environment's default project
    transactions = pd.read_gbq(sql, dialect='standard')

    latest_time = transactions['timestamp'].max()
    datediff = datetime.now() - latest_time.replace(tzinfo=None)

    transactions['timestamp'] = transactions['timestamp'] + datediff
    transactions.to_gbq(destination_table="{BIGQUERY_DATASET_NAME}.transactions", project_id=PROJECT_ID, if_exists='replace')


def update_user_account_features_timestamp():
    sql = """
    SELECT *
    FROM `feast-oss.fraud_tutorial.user_account_features`
    """

    user_features = pd.read_gbq(sql, dialect='standard')

    user_features['feature_timestamp'] = datetime.now() - timedelta(days=7)
    user_features.to_gbq(destination_table="{BIGQUERY_DATASET_NAME}.user_account_features", project_id=PROJECT_ID, if_exists='replace')


def update_user_has_fraud_timestamp():
    sql = """
    SELECT *
    FROM `feast-oss.fraud_tutorial.user_has_fraudulent_transactions`
    """

    # Run a Standard SQL query using the environment's default project
    user_has_fraud = pd.read_gbq(sql, dialect='standard')

    latest_time = user_has_fraud['feature_timestamp'].max()

    datediff = datetime.now() - latest_time.replace(tzinfo=None)

    user_has_fraud['feature_timestamp'] = user_has_fraud['feature_timestamp'] + datediff
    user_has_fraud.to_gbq(destination_table="{BIGQUERY_DATASET_NAME}.user_has_fraudulent_transactions", project_id=PROJECT_ID, if_exists='replace')


def update_timestamp():
    update_transactions_timestamp()
    update_user_account_features_timestamp()
    update_user_has_fraud_timestamp()


def ping():
    return "Pong"


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="Feature Engineering works")
#     parser.add_argument(
#         "--command", "-cmd",
#         default="ping",
#         help="Run command"
#     )

#     args = parser.parse_args()

#     if args.command == "backfill":
#         backfill_features(
#             earliest_aggregation_end_date=datetime.now() - timedelta(days=7),
#             interval=timedelta(days=1),
#             num_iterations=8
#         )
#     elif args.command == "update_timestamp":
#         update_timestamp()
#     else:
#         print(ping())
