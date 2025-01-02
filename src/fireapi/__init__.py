"""
A Python client library for the 24Fire REST API to control KVM server functions.

Author: EvickaStudio
Original documentation: https://apidocs.24fire.de/
"""

from ._async_client import AsyncFireAPI

# from ._utils import construct_url
from ._exceptions import APIAuthenticationError, APIRequestError, FireAPIError
from ._sync_client import FireAPI
from .version import __version__

__all__ = [
    "FireAPI",
    "AsyncFireAPI",
    "FireAPIError",
    "APIAuthenticationError",
    "APIRequestError",
    "__version__",
    #  "construct_url",
]
