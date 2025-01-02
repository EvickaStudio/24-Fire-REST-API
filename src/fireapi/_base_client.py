import logging
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Dict, Optional, Union

log = logging.getLogger(__name__)


class BaseFireAPIClient(ABC):
    def __init__(self, api_key: str, timeout: int = 5) -> None:
        self.api_key = api_key
        self.base_url = "https://api.24fire.de/kvm"
        self.headers = {"X-FIRE-APIKEY": api_key}
        self.timeout = timeout

    @abstractmethod
    def _request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """Make a request to the API.

        Args:
            endpoint: The API endpoint to request.
            method: The HTTP method to use.
            data: Optional data to send with the request.

        Returns:
            The response data from the API, either directly or as a coroutine.
        """
        pass
