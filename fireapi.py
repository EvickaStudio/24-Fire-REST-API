# A simple API wrapper for the 24Fire REST API
# to control basic functions of a KVM server
# with a private API key.
# Features:
# - Get server config
# - Get server status
# - Start server
# - Stop server
# - Restart server
# Author: EvickaStudio
# Original documentation: https://documenter.getpostman.com/view/18955936/2s93zB6hJu


import requests


class FireAPI:
    """
    A simple API wrapper for the 24Fire REST API
    to control basic functions of a KVM server
    with a private API key.

    Features:
    - Get server config
    - Get server status
    - Start server
    - Stop server
    - Restart server

    Author: EvickaStudio
    Original documentation: https://documenter.getpostman.com/view/18955936/2s93zB6hJu
    """

    def __init__(self, api_key):
        """
        Initializes a new instance of the FireAPI class.

            :param api_key: The private API key to use for authentication.
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

        :return: A json object containing the server configuration.
        """
        response = self.session.get(f"{self.base_url}config", timeout=self.timeout)
        return response.json()

    def get_status(self):
        """
        Retrieves the server status.

        :return: A json object containing the server status.
        """
        response = self.session.get(f"{self.base_url}status", timeout=self.timeout)
        return response.json()

    def start_server(self):
        """
        Starts the server.

        :return: A json object containing the server status.
        """
        response = self.session.post(
            f"{self.base_url}status/start", timeout=self.timeout
        )
        return response.json()

    def stop_server(self):
        """
        Stops the server.

        :return: A json object containing the server status.
        """
        response = self.session.post(
            f"{self.base_url}status/stop", timeout=self.timeout
        )
        return response.json()

    def restart_server(self):
        """
        Restarts the server.

        :return: A json object containing the server status.
        """
        response = self.session.post(
            f"{self.base_url}status/restart", timeout=self.timeout
        )
        return response.json()


if __name__ == "__main__":
    API_KEY = "your-api-key-here"
    fire_api = FireAPI(API_KEY)
    print(fire_api.get_config())
