import pytest
from tests.conftest import MockResponse
from breweries.utils.extraction_func import fetch_api

@pytest.mark.unit
def test_fetch_api_invalid_response_format(mock_request_get):
    mock_request_get.side_effect = [
        MockResponse({"error": "Unexpected response format"}, 200)
    ]
    
@pytest.mark.unit
def test_fetch_api_invalid_format_retry(mock_request_retry):
    with pytest.raises(ValueError):
        fetch_api(
            url='http://fake-api.com/breweries',
            max_retries=3,
            sleep_between_requests=0.0
        )