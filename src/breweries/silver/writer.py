from pathlib import Path
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from breweries.silver.schema import BREWERIES_SCHEMA


def write_silver(
    df: pd.DataFrame,
    silver_path: Path,
    country: str,
) -> None:
    if not country:
        raise ValueError("country must be provided")

    partition_path = silver_path / f"country={country}"
    partition_path.mkdir(parents=True, exist_ok=True)

    for field in BREWERIES_SCHEMA:
        if field.name not in df.columns:
            df[field.name] = None

    df = df[[field.name for field in BREWERIES_SCHEMA]]

    for field in BREWERIES_SCHEMA:
        if pa.types.is_string(field.type):
            df[field.name] = df[field.name].astype("string")
        elif pa.types.is_float64(field.type):
            df[field.name] = pd.to_numeric(df[field.name], errors="coerce")

    table = pa.Table.from_pandas(
        df,
        schema=BREWERIES_SCHEMA,
        preserve_index=False,
    )

    pq.write_table(
        table,
        partition_path / "breweries.parquet",
        compression="snappy",
    )
