import logging
from airflow.exceptions import AirflowException
from datetime import datetime

from breweries.bronze.ingestion import bronze_ingestion

logger = logging.getLogger(__name__)


def run_bronze_ingestion(
    url: str,
    ingestion_date: str,
    **context
) -> dict:

    logger.info("[Bronze Operator] Starting bronze ingestion")
    logger.info(f"Source URL: {url}")
    logger.info(f"Ingestion date: {ingestion_date}")

    try:
        result = bronze_ingestion(
            url=url,
            ingestion_date=ingestion_date
        )

        if result["status"] != "success":
            logger.error("Bronze ingestion returned non-success status")
            logger.error(result)

            raise AirflowException(
                f"Bronze ingestion failed with status={result['status']}"
            )

        logger.info("Bronze ingestion completed successfully")
        logger.info(f"Records ingested: {result['records']}")

        return result

    except Exception as exc:
        logger.exception("🔥 Unexpected error during Bronze ingestion")

        raise AirflowException(
            f"Bronze ingestion failed due to unexpected error: {exc}"
        )