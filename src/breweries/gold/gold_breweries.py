import sys
from pathlib import Path

from breweries.gold.reader import read_silver_all
from breweries.gold.aggregate import aggregate_breweries
from breweries.gold.writer import write_gold
from breweries.utils.local_metadata import write_metadata


def main(silver_path: str, gold_path: str, execution_date: str):
    silver_path = Path(silver_path)
    gold_path = Path(gold_path)

    df = read_silver_all(silver_path)
    aggregated = aggregate_breweries(df)

    write_gold(aggregated, gold_path)

    write_metadata(
        ingestion_date=execution_date,
        source="silver",
        status="success",
        layer="gold",
        dataset="breweries",
        partitions={},
        payload={
            "records": len(aggregated),
        },
        base_path=str(gold_path.parent),
    )

    print("Gold layer completed successfully")


if __name__ == "__main__":
    _, silver_path, gold_path, execution_date = sys.argv
    main(silver_path, gold_path, execution_date)
