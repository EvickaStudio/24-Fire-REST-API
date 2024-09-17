import logging
from typing import Dict

import aiohttp
import requests

from .exceptions import APIAuthenticationError, APIRequestError, FireAPIError
from .interface import IAPIOperations


class BaseFireAPI:
    """Base class for common functionality."""

    def __init__(self, api_key: str, timeout: int = 5):
        """Initializes a new FireAPI instance.

        Args:
            api_key (str): The private API key for authentication.
            timeout (int): Timeout for API requests in seconds (default: 5).
        """
        self.api_key = api_key
        self.base_url = "https://api.24fire.de/kvm/"
        self.headers = {"X-FIRE-APIKEY": api_key}
        self.timeout = timeout


class FireAPI(IAPIOperations, BaseFireAPI):
    """A robust API wrapper for the 24Fire REST API."""

    def __init__(self, api_key: str, timeout: int = 5):
        """Initializes a new FireAPI instance.

        Args:
            api_key (str): The private API key for authentication.
            timeout (int): Timeout for API requests in seconds (default: 5).
        """
        self.session = requests.Session()
        self.base_url = "https://api.24fire.de/kvm/"
        self.headers = {"X-FIRE-APIKEY": api_key}
        self.session.headers.update(self.headers)
        self.timeout = timeout

    def _request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Makes an API request and handles potential errors.

        Args:
            method (str): HTTP method ('GET', 'POST', etc.)
            endpoint (str): API endpoint (e.g., 'status/start').
            **kwargs: Additional keyword arguments for the request.

        Returns:
            Dict: JSON response from the server.

        Raises:
            APIRequestError: If there's an error in the request or response format.
            APIAuthenticationError: If authentication fails.
            FireAPIError: For other, general API errors.
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.request(
                method, url, headers=self.headers, json=data
            )

            if response.status_code == 401:
                raise APIAuthenticationError(
                    "Authentication failed. Check your API key."
                )
            elif response.status_code == 403:
                raise APIAuthenticationError(
                    "Access denied or this feature requires a '24fire+' subscription."
                )
            response.raise_for_status()  # Raise for other HTTP error codes

            if not response.ok:
                raise APIRequestError(
                    f"API request failed with status code {response.status_code}: {response.text}"
                )
            return response.json()

        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise FireAPIError(f"API request failed: {e}") from e

    def get_config(self) -> Dict:
        """
        Retrieve the server configuration as a JSON object.

        Usage:
            >>> config = fire_api.get_config()
            >>> print(config['data']['hostsystem']['processor'])

        Returns:
            dict: Server configuration.
        """
        return self._request("config")

    def get_status(self) -> Dict:
        """
        Retrieve the server status as a JSON object.

        Usage:
            >>> status = fire_api.get_status()
            >>> print(status)

        Returns:
            dict: Server status.
        """
        return self._request("status")

    def start_server(self) -> Dict:
        """
        Start the server and return the status as a JSON object.

        Usage:
            >>> response = fire_api.start_server()
            >>> print(response)

        Returns:
            dict: Response containing the server status.
        """
        return self._request("status/start", method="POST")

    def stop_server(self) -> Dict:
        """
        Stop the server and return the status as a JSON object.

        Usage:
            >>> response = fire_api.stop_server()
            >>> print(response)

        Returns:
            dict: Response containing the server status.
        """
        return self._request("status/stop", method="POST")

    def restart_server(self) -> Dict:
        """
        Restart the server and return the status as a JSON object.

        Usage:
            >>> response = fire_api.restart_server()
            >>> print(response)

        Returns:
            dict: Response containing the server status.
        """
        return self._request("status/restart", method="POST")

    def backup_delete(self, backup_id: str) -> Dict:
        """
        Delete a backup.

        Note: This operation is exclusive to '24fire+' subscribers.

        Args:
            backup_id (str): The ID of the backup to delete.

        Usage:
            >>> response = fire_api.backup_delete("backup_id")
            >>> print(response)

        Returns:
            dict: Response from the server.
        """
        return self._request(f"backup/delete?backup_id={backup_id}", method="DELETE")

    def backup_create(self, description: str) -> Dict:
        """
        Create a backup with a description.

        Note: This operation is exclusive to '24fire+' subscribers.

        Args:
            description (str): Description of the backup.

        Usage:
            >>> response = fire_api.backup_create("Backup description")
            >>> print(response)

        Returns:
            dict: Response from the server.
        """
        return self._request(
            "backup/create", method="POST", data={"description": description}
        )

    def backup_list(self) -> Dict:
        """
        List all backups.

        Note: This operation is exclusive to '24fire+' subscribers.

        Usage:
            >>> backups = fire_api.backup_list()
            >>> print(backups)

        Returns:
            dict: List of backups.
        """
        return self._request("backup/list")

    def timings(self) -> Dict:
        """
        Retrieve monitoring timings.

        Note: This operation is exclusive to '24fire+' subscribers.

        Usage:
            >>> timings = fire_api.timings()
            >>> print(timings)

        Returns:
            dict: Monitoring timings.
        """
        return self._request("monitoring/timings")

    def incidences(self) -> Dict:
        """
        Retrieve monitoring incidences.

        Note: This operation is exclusive to '24fire+' subscribers.

        Usage:
            >>> incidences = fire_api.incidences()
            >>> print(incidences)

        Returns:
            dict: Monitoring incidences.
        """
        return self._request("monitoring/incidences")


class AsyncFireAPI(IAPIOperations, BaseFireAPI):
    """Asynchronous API wrapper for the 24Fire REST API."""

    async def _request(
        self, endpoint: str, method: str = "GET", data: Dict = None
    ) -> Dict:
        """Makes an asynchronous API request and handles potential errors."""
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
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
                    response.raise_for_status()  # Raise for other HTTP error codes

                    if response.status != 200:
                        raise APIRequestError(
                            f"API request failed with status code {response.status}: {await response.text()}"
                        )
                    return await response.json()

            except aiohttp.ClientError as e:
                logging.error(f"Request failed: {e}")
                raise FireAPIError(f"API request failed: {e}") from e

    async def get_config(self) -> Dict:
        """
        Retrieve the server configuration as a JSON object.

        Usage:
            >>> config = await fire_api.get_config()
            >>> print(config['data']['hostsystem']['processor'])

        Returns:
            dict: Server configuration.
        """
        return await self._request("config")

    async def get_status(self) -> Dict:
        """
        Retrieve the server status as a JSON object.

        Usage:
            >>> status = await fire_api.get_status()
            >>> print(status)

        Returns:
            dict: Server status.
        """
        return await self._request("status")

    async def start_server(self) -> Dict:
        """
        Start the server and return the status as a JSON object.

        Usage:
            >>> response = await fire_api.start_server()
            >>> print(response)

        Returns:
            dict: Response containing the server status.
        """
        return await self._request("status/start", method="POST")

    async def stop_server(self) -> Dict:
        """
        Stop the server and return the status as a JSON object.

        Usage:
            >>> response = await fire_api.stop_server()
            >>> print(response)

        Returns:
            dict: Response containing the server status.
        """
        return await self._request("status/stop", method="POST")

    async def restart_server(self) -> Dict:
        """
        Restart the server and return the status as a JSON object.

        Usage:
            >>> response = await fire_api.restart_server()
            >>> print(response)

        Returns:
            dict: Response containing the server status.
        """
        return await self._request("status/restart", method="POST")

    async def backup_delete(self, backup_id: str) -> Dict:
        """
        Delete a backup.

        Note: This operation is exclusive to '24fire+' subscribers.

        Args:
            backup_id (str): The ID of the backup to delete.

        Usage:
            >>> response = await fire_api.backup_delete("backup_id")
            >>> print(response)

        Returns:
            dict: Response from the server.
        """
        return await self._request(
            f"backup/delete?backup_id={backup_id}", method="DELETE"
        )

    async def backup_create(self, description: str) -> Dict:
        """
        Create a backup with a description.

        Note: This operation is exclusive to '24fire+' subscribers.

        Args:
            description (str): Description of the backup.

        Usage:
            >>> response = await fire_api.backup_create("Backup description")
            >>> print(response)

        Returns:
            dict: Response from the server.
        """
        return await self._request(
            "backup/create", method="POST", data={"description": description}
        )

    async def backup_list(self) -> Dict:
        """
        List all backups.

        Note: This operation is exclusive to '24fire+' subscribers.

        Usage:
            >>> backups = await fire_api.backup_list()
            >>> print(backups)

        Returns:
            dict: List of backups.
        """
        return await self._request("backup/list")

    async def timings(self) -> Dict:
        """
        Retrieve monitoring timings.

        Note: This operation is exclusive to '24fire+' subscribers.

        Usage:
            >>> timings = await fire_api.timings()
            >>> print(timings)

        Returns:
            dict: Monitoring timings.
        """
        return await self._request("monitoring/timings")

    async def incidences(self) -> Dict:
        """
        Retrieve monitoring incidences.

        Note: This operation is exclusive to '24fire+' subscribers.

        Usage:
            >>> incidences = await fire_api.incidences()
            >>> print(incidences)

        Returns:
            dict: Monitoring incidences.
        """
        return await self._request("monitoring/incidences")
