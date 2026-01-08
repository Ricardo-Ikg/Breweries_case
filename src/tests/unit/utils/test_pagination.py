from breweries.utils.extraction_func import fetch_api
from tests.conftest import MockResponse
import pytest

@pytest.mark.unit
def test_fetch__api_multiple_pages_success(mock_request_get):
    mock_request_get.side_effect = [
        MockResponse([{"id": "1", "name": "Brewery1"}], 200),
        MockResponse([{"id": "2", "name": "Brewery2"}], 200),
        MockResponse([], 200)
    ]   

    data = fetch_api(
        url = 'https://api.fake.com/breweries',
        per_page = 1,
        sleep_between_requests = 0.0
    )

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['id'] == '1'
    assert data[0]['name'] == 'Brewery1'
    assert data[1]['id'] == '2'
    assert data[1]['name'] == 'Brewery2'