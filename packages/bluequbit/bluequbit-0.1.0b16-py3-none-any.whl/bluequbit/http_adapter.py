import logging

import requests
from requests.adapters import HTTPAdapter
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from urllib3 import Retry

DEFAULT_RETRY_STRATEGY = Retry(
    total=5,
    backoff_factor=1.5,
    status_forcelist=[429, 500, 502, 503, 504],
)

DEFAULT_TIMEOUT = (10.0, 100.0)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler())


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(
        self, timeout=DEFAULT_TIMEOUT, max_retries=DEFAULT_RETRY_STRATEGY, **kwargs
    ):
        self.timeout = timeout
        super().__init__(max_retries=max_retries, **kwargs)

    @retry(
        retry=retry_if_exception_type(ConnectionError),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(2),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def send(self, request, **kwargs):  # pylint: disable=arguments-differ
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


HTTP_SESSION_WITH_TIMEOUT_AND_RETRY = requests.Session()
_adapter = TimeoutHTTPAdapter()
HTTP_SESSION_WITH_TIMEOUT_AND_RETRY.mount("http://", _adapter)
HTTP_SESSION_WITH_TIMEOUT_AND_RETRY.mount("https://", _adapter)
