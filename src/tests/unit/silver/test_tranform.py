import pandas as pd
import pytest
from breweries.silver.transform import transform_breweries

@pytest.mark.unit
def test_transform_breweries():
    df = pd.DataFrame({
        "id": [1, 1, 2],
        "name": ["brewery", "brewery", "tap house"]
    })

    result = transform_breweries(df)

    assert len(result) == 2
    assert result["name"].iloc[0] == "BREWERY"
