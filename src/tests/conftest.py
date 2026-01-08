import pytest
from unittest.mock import Mock
import requests
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

sys.path.insert(0, str(SRC))


@pytest.fixture
def mock_request_get(mocker):
    return mocker.patch('breweries.utils.extraction_func.requests.get')

@pytest.fixture(autouse=True)
def disable_sleep(mocker):
    mocker.patch('breweries.utils.extraction_func.time.sleep', return_value=None)

@pytest.fixture
def mock_request_retry(mocker):
    def fake_response(*args, **kwargs):
        return MockResponse({"error": "Unexpected response format"}, 200)

    return mocker.patch("breweries.utils.extraction_func.requests.get", side_effect=fake_response)


@pytest.fixture
def mock_request_empty_success(mocker):
    responses = [
        MockResponse([{"id": 1, "name": "Brewery A"}], 200),
        MockResponse([], 200),
    ]
    return mocker.patch("breweries.utils.extraction_func.requests.get", side_effect=responses)


@pytest.fixture
def mock_request_error_then_success(mocker):
    responses = [
        MockResponse({"error": "invalid"}, 500),
        MockResponse([{"id": 99, "name": "Recovered Brewery"}], 200),
        MockResponse([], 200),
    ]
    return mocker.patch("breweries.utils.extraction_func.requests.get", side_effect=responses)

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.text = str(json_data)
    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(f'Status code: {self.status_code}')
        
    