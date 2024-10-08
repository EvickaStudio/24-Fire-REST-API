import logging
from typing import Dict

import aiohttp
import requests

from .base import BaseFireAPI
from .exceptions import APIAuthenticationError, APIRequestError, FireAPIError


class FireAPI(BaseFireAPI):
    """Synchronous API wrapper for the 24Fire REST API."""

    def __init__(self, api_key: str, timeout: int = 5):
        super().__init__(api_key, timeout)
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
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
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.request(
                method, url, json=data, timeout=self.timeout
            )

            if response.status_code == 401:
                raise APIAuthenticationError(
                    "Authentication failed. Check your API key."
                )
            elif response.status_code == 403:
                raise APIAuthenticationError(
                    "Access denied or this feature requires a '24fire+' subscription."
                )

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise FireAPIError(f"API request failed: {e}") from e


class AsyncFireAPI(BaseFireAPI):
    """Asynchronous API wrapper for the 24Fire REST API."""

    async def _request(
        self, endpoint: str, method: str = "GET", data: Dict = None
    ) -> Dict:
        """Makes an asynchronous API request and handles potential errors."""
        url = f"{self.base_url}/{endpoint}"
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.request(
                    method, url, json=data, timeout=self.timeout
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
            logging.error(f"Request failed: {e}")
            raise FireAPIError(f"API request failed: {e}") from e
