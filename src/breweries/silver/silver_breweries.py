import sys
from pathlib import Path
import logging
from breweries.silver.read_bronze import read_bronze
from breweries.silver.transform import transform_breweries
from breweries.silver.quality import validate_breweries
from breweries.silver.writer import write_silver
from breweries.utils.local_metadata import write_metadata

logger = logging.getLogger("silver_ingestion")

def main(bronze_path: str, silver_path: str, execution_date: str):
    bronze_path = Path(bronze_path)
    silver_path = Path(silver_path)

    df_raw = read_bronze(bronze_path, execution_date)
    df = transform_breweries(df_raw)

    status, quality_errors = validate_breweries(df)

    for country, df_country in df.groupby("country"):
        try:
            write_silver(
                df=df_country,
                silver_path=silver_path,
                country=country,
            )

            write_metadata(
                ingestion_date=execution_date,
                source="bronze",
                status=status,
                layer="silver",
                dataset="breweries",
                partitions={"country": country},
                error=error_message,
                payload={
                    "records": len(df_country),
                    "invalid_records": len(quality_errors),
                },
                base_path=str(silver_path.parent),
            )
            if status == "success":
                print(f"Silver completed with status={status}")

        except Exception as exc:
            error_msg = str(exc)
            logger.exception(f"Erro na Bronze: {error_msg}")

        write_metadata(
            ingestion_date=execution_date ,
            source="bronze",
            status="error",
            layer="silver",
            dataset="breweries",
            payload=None,
            base_path=str(silver_path.parent),
            error=error_msg
        )
   

if __name__ == "__main__":
    _, bronze_path, silver_path, execution_date = sys.argv
    main(bronze_path, silver_path, execution_date)
