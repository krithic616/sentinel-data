import os
import pandas as pd
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def generate_alert_summary(anomalies_df: pd.DataFrame):

    if anomalies_df is None or anomalies_df.empty:
        return "No anomalies detected."

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Compute deviation %
    anomalies_df["price_deviation_pct"] = (
        (anomalies_df["price"] - anomalies_df["historical_mean"]) 
        / anomalies_df["historical_mean"]
    ) * 100

    # Sort by absolute deviation
    anomalies_df["abs_deviation"] = anomalies_df["price_deviation_pct"].abs()
    top_anomalies = anomalies_df.sort_values(
        by="abs_deviation", ascending=False
    ).head(3)

    summary_rows = []

    for _, row in top_anomalies.iterrows():
        summary_rows.append(
            f"Product {row['product_id']} ({row['category']}) "
            f"deviated {row['price_deviation_pct']:.2f}% from baseline."
        )

    structured_context = "\n".join(summary_rows)

    system_prompt = f"""
You are a Senior Data Observability Engineer.

The following anomalies were detected at {timestamp}.

Top impacted products:
{structured_context}

Write a concise executive-level alert explaining:
- What happened
- Business impact
- Why immediate review may be required

Keep it under 4 sentences.
"""

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(system_prompt)
        return response.text.strip()

    except Exception:
        # Fallback deterministic message if LLM fails
        return (
            f"{len(anomalies_df)} pricing anomalies detected at {timestamp}. "
            f"Top deviations:\n{structured_context}"
        )
