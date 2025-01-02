import logging
from typing import Any, Dict, Optional

import aiohttp

from ._base_client import BaseFireAPIClient
from ._exceptions import APIAuthenticationError, APIRequestError
from ._utils import construct_url
from .resources import AsyncBackupResource, AsyncMonitoringResource, AsyncVMResource

log = logging.getLogger(__name__)


class AsyncFireAPI(BaseFireAPIClient):
    def __init__(self, api_key: str, timeout: int = 5) -> None:
        super().__init__(api_key, timeout)
        self.session = aiohttp.ClientSession(headers=self.headers)
        self.vm = AsyncVMResource(self)
        self.backup = AsyncBackupResource(self)
        self.monitoring = AsyncMonitoringResource(self)

    async def _request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an async request to the API.

        Args:
            endpoint: The API endpoint to request.
            method: The HTTP method to use.
            data: Optional data to send with the request.

        Returns:
            The response data from the API.

        Raises:
            APIAuthenticationError: If authentication fails.
            APIRequestError: If the request fails.
        """
        url = construct_url(self.base_url, endpoint)
        try:
            async with self.session.request(
                method,
                url,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status == 401:
                    raise APIAuthenticationError(
                        "Authentication failed. Check your API key."
                    )
                elif response.status == 403:
                    raise APIAuthenticationError(
                        "Access denied or this feature requires a '24fire+' subscription."
                    )
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            raise APIRequestError(f"API request failed: {e}") from e

    async def close(self) -> None:
        """Close the aiohttp session."""
        await self.session.close()

    async def __aenter__(self) -> "AsyncFireAPI":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
