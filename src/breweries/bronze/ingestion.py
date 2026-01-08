import logging
from breweries.utils.extraction_func import fetch_api
from breweries.utils.local_writer import save_to_local
from breweries.utils.local_metadata import write_metadata

logger = logging.getLogger("bronze_ingestion")


def bronze_ingestion(
    *,
    url: str,
    ingestion_date: str,
    base_path: str = "data/bronze/breweries"
) -> dict:

    year, month, day = ingestion_date.split("-")

    try:
        logger.info("Iniciando ingestão Bronze")

        data = fetch_api(url)
        records = len(data)
        status = "success" if records > 0 else "empty"

        file_path = save_to_local(
            data=data,
            year=year,
            month=month,
            day=day,
            base_path=base_path
        )

        write_metadata(
            ingestion_date=ingestion_date,
            source="api",
            status="success",
            layer="bronze",
            dataset="breweries",
            partitions={
                "year": year,
                "month": month,
                "day": day,
            },
            payload={"records": records},
        )


        logger.info(f"Bronze finalizada com sucesso | records={records}")

        return {
            "layer": "bronze",
            "status": status,
            "source": url,
            "ingestion_date": ingestion_date,
            "path": file_path
        }

    except Exception as exc:
        error_msg = str(exc)

        write_metadata(
            ingestion_date=ingestion_date,
            source=url,
            status="error",
            layer="bronze",
            dataset="breweries",
            payload=None,
            base_path=base_path,
            error=error_msg
        )

        logger.exception(f"Erro na Bronze: {error_msg}")
        raise


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        raise ValueError("Uso: ingestion.py <url> <ingestion_date>")

    url = sys.argv[1]
    ingestion_date = sys.argv[2]

    bronze_ingestion(
        url=url,
        ingestion_date=ingestion_date,
        base_path="/opt/airflow/data/bronze/breweries"
    )
