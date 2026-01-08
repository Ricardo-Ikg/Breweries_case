import pandas as pd

def transform_breweries(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["name"] = df["name"].str.upper()
    df = df.drop_duplicates(subset=["id"])
    return df
