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

from .api import FireAPI
from .exceptions import APIAuthenticationError, APIRequestError, FireAPIError

if __name__ == "__main__":
    API_KEY = "your-api-key-here"
    try:
        fire_api = FireAPI(API_KEY)
        print(fire_api.get_config())
    except FireAPIError as e:
        print(f"An error occurred: {e}")
