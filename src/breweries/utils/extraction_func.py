import requests
import logging
from typing import Any, Dict, List
import time
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def fetch_api(
    url: str,
    page_param: str = "page",
    per_page_param: str = "per_page",
    per_page: int = 200,
    start_page: int = 1,
    max_retries: int = 3,
    timeout: int = 30,
    sleep_between_requests: float = 0.5
) -> List[Dict[str, Any]]:

    data_list: List[Dict[str, Any]] = []
    page = start_page

    logger.info("Starting extraction", extra={"url": url})

    while True:

        params = {page_param: page, per_page_param: per_page}

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, params=params, timeout=timeout)
                response.raise_for_status()
                data = response.json()

                if not isinstance(data, list):
                    raise ValueError("Unexpected response format")

                break

            except (RequestException, ValueError) as exc:
                logger.warning(
                    "Attempt failed",
                    extra={"url": url, "page": page, "attempt": attempt, "error": str(exc)},
                )

                if attempt == max_retries:
                    raise ValueError("Max retries reached, aborting extraction")
                    

                time.sleep(sleep_between_requests)

        if not data:
            logger.info("No more data, ending extraction.")
            break

        data_list.extend(data)
        page += 1
        time.sleep(sleep_between_requests)

    logger.info("Completed extraction", extra={"total_records": len(data_list)})
    return data_list
