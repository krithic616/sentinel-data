import sys
from datetime import datetime

from src.generator import create_historical_data, generate_daily_data
from src.validator import validate_daily_data
from src.anomaly_detector import detect_anomalies
from src.llm_alert import generate_alert_summary
from src.telegram_alert import send_telegram_alert
from src.logger_config import get_logger

logger = get_logger()


def run_pipeline():
    logger.info("Pipeline started", extra={"stage": "startup"})

    try:
        create_historical_data()
        generate_daily_data()
        logger.info("Data generation completed", extra={"stage": "ingestion"})

        validation_passed = validate_daily_data()

        if not validation_passed:
            logger.error("Validation failed", extra={"stage": "validation"})

            send_telegram_alert(
                "Deterministic validation failed.\n"
                f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )

            sys.exit(1)

        logger.info("Validation passed", extra={"stage": "validation"})

        flag, anomalies_df = detect_anomalies()

        if flag:
            logger.warning("Anomalies detected", extra={"stage": "ml_detection"})

            
            summary = generate_alert_summary(anomalies_df)

            send_telegram_alert(summary, anomalies_df)

        else:
            logger.info("No anomalies detected", extra={"stage": "ml_detection"})

        logger.info("Pipeline completed successfully", extra={"stage": "completion"})

    except Exception as e:
        logger.error(
            f"Pipeline crashed: {str(e)}",
            extra={"stage": "system_failure"}
        )

        send_telegram_alert(
            f"Pipeline crashed:\n{str(e)}\n"
            f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
        )

        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()
