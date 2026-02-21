import os
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv



load_dotenv()


DATA_DIR = "data"
DATA_PATH = os.path.join(DATA_DIR, "historical_prices.csv")
DAILY_PATH = os.path.join(DATA_DIR, "daily_prices.csv")


PRODUCTION_MODE = os.getenv("PRODUCTION_MODE", "false").lower() == "true"



def create_historical_data(num_products=500):
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(DATA_PATH) and os.path.getsize(DATA_PATH) > 0:
        print("Historical data already exists.")
        return

    print("Creating historical baseline data...")

    np.random.seed(42)

    product_ids = [f"P{i:04d}" for i in range(1, num_products + 1)]
    categories = ["Shoes", "Electronics", "Clothing", "Accessories"]

    data = {
        "product_id": product_ids,
        "category": np.random.choice(categories, num_products),
        "price": np.random.normal(loc=2000, scale=500, size=num_products),
        "competitor_price": np.random.normal(loc=2100, scale=500, size=num_products),
        "date": datetime.today().strftime("%Y-%m-%d")
    }

    df = pd.DataFrame(data)

    df["price"] = df["price"].clip(lower=100)
    df["competitor_price"] = df["competitor_price"].clip(lower=100)

    df.to_csv(DATA_PATH, index=False)
    print("Historical data created successfully.")



def generate_daily_data(anomaly_probability=0.02):
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Historical data not found.")

    print("Generating daily data snapshot...")

    df = pd.read_csv(DATA_PATH)

    
    df["price"] = df["price"] * np.random.normal(1.0, 0.02, len(df))
    df["competitor_price"] = df["competitor_price"] * np.random.normal(1.0, 0.02, len(df))
    df["date"] = datetime.today().strftime("%Y-%m-%d")

    num_anomalies = 0  

    if not PRODUCTION_MODE:
        num_anomalies = int(len(df) * anomaly_probability)

        if num_anomalies > 0:
            anomaly_indices = np.random.choice(df.index, num_anomalies, replace=False)

            for idx in anomaly_indices:
                anomaly_type = np.random.choice(["spike", "drop", "null"])

                if anomaly_type == "spike":
                    df.at[idx, "price"] *= 5
                elif anomaly_type == "drop":
                    df.at[idx, "price"] *= 0.1
                elif anomaly_type == "null":
                    df.at[idx, "price"] = np.nan

        print(f"Daily data generated with {num_anomalies} anomalies (TEST MODE).")
    else:
        print("Daily data generated (PRODUCTION MODE - no synthetic anomalies).")

    df.to_csv(DAILY_PATH, index=False)


if __name__ == "__main__":
    create_historical_data()
    generate_daily_data()
