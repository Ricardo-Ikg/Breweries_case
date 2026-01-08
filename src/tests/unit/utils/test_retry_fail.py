import pytest
from requests.exceptions import RequestException
from unittest.mock import patch

from breweries.utils.extraction_func import fetch_api


@pytest.mark.unit
def test_fetch_api_retry_fail_fast():
    with patch(
        "breweries.utils.extraction_func.requests.get",
        side_effect=RequestException("API down"),
    ):
        with pytest.raises(ValueError, match="Max retries reached"):
            fetch_api(
                url="http://fake-api",
                max_retries=2,
                sleep_between_requests=0,  # 👈 CRÍTICO
            )
