"""
Fraud Model logic
"""

from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import joblib

FEATURES = [
    "user_transaction_count_7d:transaction_count_7d",
    "user_account_features:credit_score",
    "user_account_features:account_age_days",
    "user_account_features:user_has_2fa_installed",
    "user_has_fraudulent_transactions:user_has_fraudulent_transactions_7d"
]


class FraudModel:
    """
    Realtime fraud model implementation
    """

    def __init__(self, store, model_path):
        self.store = store
        self.model_service = None
        self.model_path = model_path

    def set_model_service(self, model_service):
        self.model_service = model_service

    def prepare_training_data(self):
        """
        Prepare training dataset
        """
        # Get training data
        now = datetime.now()
        two_days_ago = datetime.now() - timedelta(days=2)
        training_data = self.store.get_historical_features(
            entity_df=f"""select src_account as user_id, timestamp as event_timestamp, is_fraud
            from
                feast-oss.fraud_tutorial.transactions
            where
                timestamp between timestamp('{two_days_ago.isoformat()}')
                and timestamp('{now.isoformat()}')""",
            features=FEATURES,
            full_feature_names=True
        ).to_df()

        return training_data

    def train(self, training_data):
        """
        Training
        """
        # Drop stray nulls
        training_data.dropna(inplace=True)

        # Select training matrices
        X = training_data[[f.replace(":", "__") for f in FEATURES]]
        y = training_data["is_fraud"]

        # Train a simple SVC model
        model = LinearRegression()
        model.fit(X, y)

        joblib.dump(model, self.model_path)

        return model, X, y

    def predict(self, entity_rows):
        """
        Online prediction
        """
        feature_vector = self.store.get_online_features(
            features=FEATURES,
            entity_rows=entity_rows,
            full_feature_names=True
        ).to_df()

        # Delete entity keys
        feature_vector.pop("user_id")

        # Flatten response from Feast
        instances = feature_vector[[f.replace(":", "__") for f in FEATURES]]
        response = self.model_service.predict(instances)

        return response, feature_vector
