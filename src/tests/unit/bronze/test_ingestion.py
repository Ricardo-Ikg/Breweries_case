import pytest
from unittest.mock import patch

from breweries.bronze.ingestion import bronze_ingestion


@pytest.mark.unit
def test_bronze_ingestion_creates_file(tmp_path):
    with patch(
        "breweries.bronze.ingestion.fetch_api",
        return_value=[{"id": 1}],
    ):
        result = bronze_ingestion(
            url="http://fake-api",
            ingestion_date="2026-01-01",
            base_path=str(tmp_path),
        )

    # valida retorno
    assert result["status"] == "success"
    assert result["layer"] == "bronze"

    # valida que arquivo foi criado
    files = list(tmp_path.rglob("*.json"))
    assert files
