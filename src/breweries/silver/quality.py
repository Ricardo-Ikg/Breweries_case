from pandera.errors import SchemaErrors
from breweries.silver.quality_schema import BREWERIES_QUALITY_SCHEMA

def validate_breweries(df):
    try:
        BREWERIES_QUALITY_SCHEMA.validate(df, lazy=True)
        return "success", None
    except SchemaErrors as exc:
        return "quality_failed", exc.failure_cases.to_dict(orient="records")
