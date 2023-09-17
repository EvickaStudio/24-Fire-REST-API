"""
A simple API wrapper for the 24Fire REST API to control basic functions of a KVM server with a private API key.

Author: EvickaStudio
Original documentation: [https://documenter.getpostman.com/view/18955936/2s93zB6hJu](https://documenter.getpostman.com/view/18955936/2s93zB6hJu)

Usage:

   >>> from fireapi import FireAPI
   >>> API_KEY = "your-api-key-here"
   >>> fire_api = FireAPI(API_KEY)

   >>> # Get server configuration
   >>> config = fire_api.get_config()
   >>> print(config)
   {'status': 'success', 'requestID': '....
    >>> datacenter = config["data"]["hostsystem"]["datacenter"]["name"]
    >>> processor = config["data"]["hostsystem"]["processor"]
"""

import requests
import logging

class FireAPI:
    """
    A simple API wrapper for the 24Fire REST API to control basic functions of a KVM server with a private API key.

    Features:
    - Get server config
    - Get server status
    - Start server
    - Stop server
    - Restart server
    """
    def __init__(self, api_key):
        """
        Initializes a new instance of the FireAPI class.

        Args:
            api_key (str): The private API key to use for authentication.
        """
        self.api_key = api_key
        self.base_url = "https://api.24fire.de/kvm/"
        self.headers = {"X-FIRE-APIKEY": api_key}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.timeout = 5

    def get_config(self):
        """
        Retrieves the server configuration.

        Returns:
            dict: A json object containing the server configuration.
        """
        try:
            response = self.session.get(f"{self.base_url}config", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving server configuration: {e}")
            return None

    def get_status(self):
        """
        Retrieves the server status.

        Returns:
            dict: A json object containing the server status.
        """
        try:
            response = self.session.get(f"{self.base_url}status", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving server status: {e}")
            return None

    def start_server(self):
        """
        Starts the server.

        Returns:
            dict: A json object containing the server status.
        """
        try:
            response = self.session.post(f"{self.base_url}status/start", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error starting server: {e}")
            return None

    def stop_server(self):
        """
        Stops the server.

        Returns:
            dict: A json object containing the server status.
        """
        try:
            response = self.session.post(f"{self.base_url}status/stop", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error stopping server: {e}")
            return None

    def restart_server(self):
        """
        Restarts the server.

        Returns:
            dict: A json object containing the server status.
        """
        try:
            response = self.session.post(f"{self.base_url}status/restart", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error restarting server: {e}")
            return None


if __name__ == "__main__":
    API_KEY = "your-api-key-here"
    logging.basicConfig(level=logging.INFO)
    fire_api = FireAPI(API_KEY)
    print(fire_api.get_config())