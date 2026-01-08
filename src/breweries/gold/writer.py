from pathlib import Path
import pandas as pd

def write_gold(df: pd.DataFrame, gold_path: Path) -> None:
    gold_path.mkdir(parents=True, exist_ok=True)

    output_path = gold_path / "breweries_aggregated.parquet"
    df.to_parquet(output_path, index=False)
