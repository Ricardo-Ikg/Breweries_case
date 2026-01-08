from pathlib import Path
import pandas as pd
import pyarrow.dataset as ds


def read_silver_all(silver_path: str | Path) -> pd.DataFrame:
    dataset = ds.dataset(
        silver_path,
        format="parquet",
        partitioning="hive",
    )

    table = dataset.to_table()
    return table.to_pandas()
