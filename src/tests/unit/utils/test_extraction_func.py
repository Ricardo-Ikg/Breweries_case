from breweries.utils.extraction_func import fetch_api
from tests.conftest import MockResponse
import pytest


@pytest.mark.unit
def test_fetch_api_success(mock_request_get):
    mock_request_get.side_effect = [
        MockResponse([{"id": "1", "name": "Brewery"}],200),
        MockResponse([], 200)
    ]   


    data = fetch_api(
        url = 'http://fake-api',
        per_page = 200,
        sleep_between_requests = 0.0
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == '1'
    assert data[0]['name'] == 'Brewery'