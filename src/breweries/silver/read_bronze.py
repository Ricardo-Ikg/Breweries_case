from pathlib import Path
import pandas as pd


def read_bronze(
    bronze_path: Path,
    execution_date: str,
) -> pd.DataFrame:
    year, month, day = execution_date.split("-")

    path = (
        bronze_path
        / f"year={year}"
        / f"month={month}"
        / f"day={day}"
        / "breweries.json"
    )

    if not path.exists():
        raise FileNotFoundError(f"Bronze file not found: {path}")

    return pd.read_json(path)
