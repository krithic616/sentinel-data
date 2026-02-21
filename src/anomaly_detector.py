import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

DATA_DIR = "data"
HISTORICAL_PATH = os.path.join(DATA_DIR, "historical_prices.csv")
DAILY_PATH = os.path.join(DATA_DIR, "daily_prices.csv")

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest.pkl")


def detect_anomalies():

    if not os.path.exists(HISTORICAL_PATH):
        raise FileNotFoundError("Historical data not found.")

    if not os.path.exists(DAILY_PATH):
        raise FileNotFoundError("Daily data not found.")

    print("Running probabilistic anomaly detection...")

    os.makedirs(MODEL_DIR, exist_ok=True)

    historical_df = pd.read_csv(HISTORICAL_PATH)
    daily_df = pd.read_csv(DAILY_PATH)

   

    historical_means = (
        historical_df.groupby("product_id")["price"]
        .mean()
        .reset_index()
        .rename(columns={"price": "historical_mean"})
    )

    daily_df = daily_df.merge(
        historical_means,
        on="product_id",
        how="left"
    )

    
    daily_df["historical_mean"] = daily_df["historical_mean"].fillna(
        daily_df["price"]
    )

   
    model = IsolationForest(
        contamination=0.02,
        random_state=42
    )

    model.fit(historical_df[["price"]])

    daily_df["anomaly_flag"] = model.predict(daily_df[["price"]])

    anomalies = daily_df[daily_df["anomaly_flag"] == -1].copy()

 

    if not anomalies.empty:
        anomalies["deviation_percent"] = (
            (anomalies["price"] - anomalies["historical_mean"])
            / anomalies["historical_mean"]
        ) * 100

        anomalies["deviation_percent"] = anomalies["deviation_percent"].round(2)

    print(f"Anomalies detected: {len(anomalies)}")

    return len(anomalies) > 0, anomalies
