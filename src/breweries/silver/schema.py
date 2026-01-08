import pyarrow as pa

BREWERIES_SCHEMA = pa.schema([
    pa.field("id", pa.string(), nullable=True),
    pa.field("name", pa.string(), nullable=True),
    pa.field("brewery_type", pa.string(), nullable=True),
    pa.field("street", pa.string(), nullable=True),
    pa.field("city", pa.string(), nullable=True),
    pa.field("state", pa.string(), nullable=True),
    pa.field("postal_code", pa.string(), nullable=True),
    pa.field("country", pa.string(), nullable=True),
    pa.field("longitude", pa.float64(), nullable=True),
    pa.field("latitude", pa.float64(), nullable=True),
])
