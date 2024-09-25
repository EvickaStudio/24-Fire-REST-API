import logging
from typing import Any, Coroutine, Dict, Optional

import aiohttp
import requests

from .base import BaseFireAPI
from .exceptions import APIAuthenticationError, FireAPIError


class FireAPI(BaseFireAPI):
    """Synchronous API wrapper for the 24Fire REST API."""

    def __init__(self, apiKey: str, timeout: int = 5) -> None:
        super().__init__(apiKey, timeout)
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _construct_url(self, endpoint: str) -> str:
        return f"{self.baseUrl}/{endpoint}"

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code == 401:
            raise APIAuthenticationError("Authentication failed. Check your API key.")
        elif response.status_code == 403:
            raise APIAuthenticationError(
                "Access denied or this feature requires a '24fire+' subscription."
            )

        response.raise_for_status()
        return response.json()

    def _request(
        self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Makes an API request and handles potential errors.
        Args:
            endpoint (str): The API endpoint to send the request to.
            method (str, optional): The HTTP method to use for the request. Defaults to "GET".
            data (Dict, optional): The data to send with the request, if any. Defaults to None.
        Returns:
            Dict: The JSON response from the API.
        Raises:
            APIAuthenticationError: If authentication fails or access is denied.
            FireAPIError: If the request fails for any other reason.
        """
        url = self._construct_url(endpoint)
        try:
            response = self.session.request(
                method, url, json=data, timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.RequestException as e:
            logging.error(f"Request to {url} with method {method} failed: {e}")
            raise FireAPIError(f"API request failed: {e}") from e
        finally:
            self.session.close()


class AsyncFireAPI(BaseFireAPI):
    """Asynchronous API wrapper for the 24Fire REST API."""

    def _construct_url(self, endpoint: str) -> str:
        return f"{self.baseUrl}/{endpoint}"

    async def _handle_response(
        self, response: aiohttp.ClientResponse
    ) -> Dict[str, Any]:
        if response.status == 401:
            raise APIAuthenticationError("Authentication failed. Check your API key.")
        elif response.status == 403:
            raise APIAuthenticationError(
                "Access denied or this feature requires a '24fire+' subscription."
            )

        response.raise_for_status()
        return await response.json()

    async def _request(  # type: ignore[override]
        self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None
    ) -> Coroutine[Any, Any, Dict[str, Any]]:
        """
        Makes an asynchronous API request and handles potential errors.
        Args:
            endpoint (str): The API endpoint to send the request to.
            method (str, optional): The HTTP method to use for the request. Defaults to "GET".
            data (Dict, optional): The data to send with the request, if any. Defaults to None.
        Returns:
            Coroutine: A coroutine that resolves to the JSON response from the API.
        Raises:
            APIAuthenticationError: If authentication fails or access is denied.
            FireAPIError: If the request fails for any other reason.
        """
        url = self._construct_url(endpoint)
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.request(
                    method, url, json=data, timeout=self.timeout
                ) as response:
                    return await self._handle_response(response)  # type: ignore[return-value]
        except aiohttp.ClientError as e:
            logging.error(f"Request to {url} with method {method} failed: {e}")
            raise FireAPIError(f"API request failed: {e}") from e
