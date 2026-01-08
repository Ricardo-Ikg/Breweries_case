from pathlib import Path
import pandas as pd
import pytest
import json

from breweries.silver.silver_breweries import main as silver_main
from breweries.gold.gold_breweries import main as gold_main

@pytest.mark.integration
def create_bronze_file(bronze_path: Path, execution_date: str):
    year, month, day = execution_date.split("-")

    path = (
        bronze_path
        / f"year={year}"
        / f"month={month}"
        / f"day={day}"
    )
    path.mkdir(parents=True, exist_ok=True)

    data = [
        {
            "id": "1",
            "name": "brew one",
            "brewery_type": "micro",
            "state": "CA",
        },
        {
            "id": "2",
            "name": "brew two",
            "brewery_type": "micro",
            "state": "CA",
        },
        {
            "id": "3",
            "name": "brew three",
            "brewery_type": "regional",
            "state": "NY",
        },
    ]

    with open(path / "breweries.json", "w") as f:
        json.dump(data, f)


@pytest.mark.integration
def test_silver_to_gold_pipeline(tmp_path):
    execution_date = "2026-01-07"

    bronze_path = tmp_path / "bronze"
    silver_path = tmp_path / "silver"
    gold_path = tmp_path / "gold"

    create_bronze_file(bronze_path, execution_date)

    silver_main(
        bronze_path=str(bronze_path),
        silver_path=str(silver_path),
        execution_date=execution_date,
    )

    silver_files = list(silver_path.glob("*.parquet"))
    assert silver_files, "Silver parquet was not generated"

    silver_df = pd.read_parquet(silver_files[0], engine="fastparquet")
    assert len(silver_df) == 3
    assert silver_df["name"].str.isupper().all()

    gold_main(
        silver_path=str(silver_path),
        gold_path=str(gold_path),
        execution_date=execution_date,
    )

    gold_file = gold_path / "breweries_aggregations.parquet"
    assert gold_file.exists(), "Gold aggregation not generated"

    gold_df = pd.read_parquet(gold_file)

    by_state = gold_df[gold_df["metric"] == "by_state"]
    by_type = gold_df[gold_df["metric"] == "by_type"]

    assert by_state.loc[by_state["state"] == "CA", "breweries_count"].iloc[0] == 2
    assert by_state.loc[by_state["state"] == "NY", "breweries_count"].iloc[0] == 1

    assert by_type.loc[by_type["brewery_type"] == "micro", "breweries_count"].iloc[0] == 2
    assert by_type.loc[by_type["brewery_type"] == "regional", "breweries_count"].iloc[0] == 1
