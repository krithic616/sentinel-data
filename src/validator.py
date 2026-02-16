import pandas as pd

DAILY_PATH = "data/daily_prices.csv"


def validate_daily_data():
    print("Running deterministic validation...")

    df = pd.read_csv(DAILY_PATH)

    errors = []

    # Rule 1: price must not be null
    if df["price"].isnull().any():
        errors.append("Null values detected in price column.")

    # Rule 2: price must be greater than 0
    if (df["price"] <= 0).any():
        errors.append("Non-positive values detected in price column.")

    # Rule 3: product_id must be unique
    if df["product_id"].duplicated().any():
        errors.append("Duplicate product_id values detected.")

    if len(errors) == 0:
        print("Validation Passed.")
        return True
    else:
        print("Validation Failed.")
        print("\n--- Validation Errors ---")
        for err in errors:
            print("-", err)
        return False


if __name__ == "__main__":
    validate_daily_data()
