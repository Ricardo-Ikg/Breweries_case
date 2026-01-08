import pandas as pd

def aggregate_breweries(df: pd.DataFrame) -> pd.DataFrame:
    aggregated = (
        df
        .groupby(["country", "state", "brewery_type"], dropna=False)
        .size()
        .reset_index(name="breweries_count")
    )

    return aggregated
