import pandas as pd
import pytest
from breweries.silver.quality import validate_breweries

@pytest.mark.integration
def test_silver_quality_fails_on_null_id():
    df = pd.DataFrame({
        "id": [1, None],
        "name": ["A", "B"]
    })

    status, errors = validate_breweries(df)

    # valida status geral
    assert status == "quality_failed"

    # valida que houve erros
    assert errors
    assert isinstance(errors, list)

    # valida que existe erro na coluna id
    error_columns = {error.get("column") for error in errors}
    assert "id" in error_columns