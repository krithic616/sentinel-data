import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def format_table(df):
    """
    Dynamically builds aligned table for Telegram.
    """

    if df is None or df.empty:
        return ""

    # Select required columns safely
    columns = ["product_id", "category", "price", "deviation_percent"]
    df = df[columns].copy()

    # Format deviation
    df["deviation_percent"] = df["deviation_percent"].apply(
        lambda x: f"{x:+.2f}%"
    )

    # Convert all to string
    df = df.astype(str)

    # Calculate max column widths
    col_widths = {
        col: max(df[col].map(len).max(), len(col))
        for col in df.columns
    }

    # Build header
    header = " | ".join(
        col.ljust(col_widths[col]) for col in df.columns
    )

    separator = "-+-".join(
        "-" * col_widths[col] for col in df.columns
    )

    # Build rows
    rows = []
    for _, row in df.iterrows():
        row_line = " | ".join(
            row[col].ljust(col_widths[col])
            for col in df.columns
        )
        rows.append(row_line)

    table = header + "\n" + separator + "\n" + "\n".join(rows)

    return f"\n\n```\n{table}\n```"


def send_telegram_alert(message, anomalies_df=None):
    """
    Sends formatted Telegram alert.
    """

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    full_message = f"{message}\n\nTime: {timestamp}"

    # Attach formatted table if available
    if anomalies_df is not None and not anomalies_df.empty:
        full_message += format_table(anomalies_df.head(5))

    payload = {
        "chat_id": CHAT_ID,
        "text": full_message,
        "parse_mode": "Markdown"
    }

    response = requests.post(TELEGRAM_URL, json=payload)

    if response.status_code == 200:
        print("Telegram alert sent successfully.")
    else:
        print("Failed to send Telegram alert.")
        print(response.text)
