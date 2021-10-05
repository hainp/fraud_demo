from feast import FeatureStore
from fraud_model import FraudModel
import joblib


def test_main():
    store = FeatureStore(repo_path="./features/dev")
    fm = FraudModel(store, model_path="./build/model.joblib")
    df = fm.prepare_training_data()
    m, train_set, _ = fm.train(df)

    samples = train_set.iloc[:2]

    rs = m.predict(samples)

    assert len(rs) == 2, rs


def test_predict():
    store = FeatureStore(repo_path="./features/dev")
    fm = FraudModel(store, model_path="./build/model.joblib")

    m = joblib.load("./build/model.joblib")
    fm.set_model_service(m)

    r, v = fm.predict([{"user_id": "v5zlw0"}])

    assert r[0] >= 0.04, r
    assert v is not None, v
