import pandas as pd
import pytest

from breweries.gold.gold_breweries import aggregate_breweries


@pytest.mark.unit
def test_gold_aggregation():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "state": ["CA", "CA", "NY"],
        "brewery_type": ["micro", "micro", "brewpub"],
    })

    result = aggregate_breweries(df)

    by_state = result[result["metric"] == "by_state"]
    by_type = result[result["metric"] == "by_type"]


    assert len(by_state) == 2
    assert by_state.loc[
        by_state["state"] == "CA", "breweries_count"
    ].iloc[0] == 2
    assert by_state.loc[
        by_state["state"] == "NY", "breweries_count"
    ].iloc[0] == 1

    assert len(by_type) == 2
    assert by_type.loc[
        by_type["brewery_type"] == "micro", "breweries_count"
    ].iloc[0] == 2
    assert by_type.loc[
        by_type["brewery_type"] == "brewpub", "breweries_count"
    ].iloc[0] == 1
