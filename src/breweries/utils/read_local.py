from pathlib import Path
from pathlib import Path
import pandas as pd


def reader(
    silver_path: Path,
    country: str | None = None,
) -> pd.DataFrame:
    base = Path(silver_path)

    if country:
        path = base / f"country={country}"
    else:
        path = base

    return pd.read_parquet(path)

def read_metadata_local(
    *,
    layer: str,
    dataset: str,
    country: str,
    base_path: str = "/opt/airflow/data",
) -> dict:
    import json
    from pathlib import Path

    path = (
        Path(base_path)
        / layer
        / dataset
        / f"country={country}"
        / "metadata.json"
    )

    if not path.exists():
        raise FileNotFoundError(f"Metadata not found: {path}")

    with open(path) as f:
        return json.load(f)


def list_silver_countries(
    *,
    dataset: str,
    base_path: str = "/opt/airflow/data",
) -> list[str]:
    base = Path(base_path) / "silver" / dataset
    return [
        p.name.replace("country=", "")
        for p in base.glob("country=*")
        if p.is_dir()
    ]
