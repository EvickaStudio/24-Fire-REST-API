"""
A simple API wrapper for the 24Fire REST API to control basic functions of a
KVM server with a private API key.

Author: EvickaStudio
Original documentation: https://apidocs.24fire.de/

Usage:

   >>> from fireapi import FireAPI
   >>> apiKey = "your-api-key-here"
   >>> fireApi = FireAPI(apiKey)

   >>> # Retrieve server configuration
   >>> config = fireApi.vm.getConfig()
   >>> print(config)
   {'status': 'success', 'requestID': '....
   >>> datacenter = config["data"]["hostsystem"]["datacenter"]["name"]
   >>> processor = config["data"]["hostsystem"]["processor"]
   >>> # Retrieve server configuration asynchronously
   >>> config = await async_fireApi.vm.getConfig()
   >>> print(config)
   {'status': 'success', 'requestID': '....
   >>> datacenter = config["data"]["hostsystem"]["datacenter"]["name"]
   >>> processor = config["data"]["hostsystem"]["processor'}
"""

from .api import AsyncFireAPI, FireAPI
from .exceptions import APIAuthenticationError, APIRequestError, FireAPIError
