"""
A simple API wrapper for the 24Fire REST API to control basic functions of a KVM server with a private API key.

Author: EvickaStudio
Original documentation: [https://documenter.getpostman.com/view/18955936/2s93zB6hJu](https://documenter.getpostman.com/view/18955936/2s93zB6hJu)

Usage:

   >>> from fireapi import FireAPI
   >>> API_KEY = "your-api-key-here"
   >>> fire_api = FireAPI(API_KEY)

   >>> # Retrieve server configuration
   >>> config = fire_api.get_config()
   >>> print(config)
   {'status': 'success', 'requestID': '....
   >>> datacenter = config["data"]["hostsystem"]["datacenter"]["name"]
   >>> processor = config["data"]["hostsystem"]["processor"]
"""

import requests
import logging


class FireAPIError(Exception):
    """Custom exception for FireAPI. Raised when an API request fails."""

    pass


class FireAPI:
    """A robust API wrapper for the 24Fire REST API."""

    def __init__(self, api_key, timeout=5):
        """
        Initialize a new FireAPI instance.

        Usage:
            >>> fire_api = FireAPI("your-api-key-here")

        Args:
            api_key (str): The private API key for authentication.
            timeout (int): Timeout for API requests in seconds.
        """
        self.api_key = api_key
        self.base_url = "https://api.24fire.de/kvm/"
        self.headers = {"X-FIRE-APIKEY": api_key}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.timeout = timeout

    def _make_request(self, method, endpoint, **kwargs):
        """
        Make an API request and return the JSON response.

        Args:
            method (str): HTTP method ('GET', 'POST', etc.)
            endpoint (str): API endpoint (e.g., 'status/start').
            **kwargs: Additional keyword arguments for the request.

        Returns:
            dict: JSON response from the server.

        Raises:
            FireAPIError: If the API request fails.
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise FireAPIError(f"API request failed: {e}") from e

    def get_config(self):
        """
        Retrieve the server configuration as a JSON object.

        Usage:
            >>> config = fire_api.get_config()
            >>> print(config['data']['hostsystem']['processor'])

        Returns:
            dict: Server configuration.
        """
        return self._make_request("GET", "config")

    def get_status(self):
        """
        Retrieve the server status as a JSON object.

        Usage:
            >>> status = fire_api.get_status()
            >>> print(status)

        Returns:
            dict: Server status.
        """
        return self._make_request("GET", "status")

    def start_server(self):
        """
        Start the server and return the status as a JSON object.

        Usage:
            >>> response = fire_api.start_server()
            >>> print(response)

        Returns:
            dict: Response containing the server status.
        """
        return self._make_request("POST", "status/start")

    def stop_server(self):
        """
        Stop the server and return the status as a JSON object.

        Usage:
            >>> response = fire_api.stop_server()
            >>> print(response)

        Returns:
            dict: Response containing the server status.
        """
        return self._make_request("POST", "status/stop")

    def restart_server(self):
        """
        Restart the server and return the status as a JSON object.

        Usage:
            >>> response = fire_api.restart_server()
            >>> print(response)

        Returns:
            dict: Response containing the server status.
        """
        return self._make_request("POST", "status/restart")


if __name__ == "__main__":
    API_KEY = "your-api-key-here"
    logging.basicConfig(level=logging.INFO)
    try:
        fire_api = FireAPI(API_KEY)
        print(fire_api.get_config())
    except FireAPIError as e:
        logging.error(f"An error occurred: {e}")
