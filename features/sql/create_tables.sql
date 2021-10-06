CREATE TABLE `{PROJECT_ID}.{BIGQUERY_DATASET_NAME}.transactions` AS (
  SELECT * FROM `feast-oss.fraud_tutorial.transactions`
)
------
CREATE TABLE `{PROJECT_ID}.{BIGQUERY_DATASET_NAME}.user_account_features` AS (
  SELECT * FROM `feast-oss.fraud_tutorial.user_account_features`
)
------
CREATE TABLE `{PROJECT_ID}.{BIGQUERY_DATASET_NAME}.user_has_fraudulent_transactions` AS (
  SELECT * FROM `feast-oss.fraud_tutorial.user_has_fraudulent_transactions`
)
