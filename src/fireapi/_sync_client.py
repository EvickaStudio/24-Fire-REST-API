from typing import Any, Dict, Optional

import requests

from ._base_client import BaseFireAPIClient
from ._exceptions import APIAuthenticationError, APIRequestError
from ._utils import construct_url
from .resources import BackupResource, MonitoringResource, VMResource


class FireAPI(BaseFireAPIClient):
    def __init__(self, api_key: str, timeout: int = 5) -> None:
        super().__init__(api_key, timeout)
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.vm = VMResource(self)
        self.backup = BackupResource(self)
        self.monitoring = MonitoringResource(self)

    def _request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = construct_url(self.base_url, endpoint)
        try:
            response = self.session.request(
                method, url, json=data, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            if response.status_code == 401:
                raise APIAuthenticationError(
                    "Authentication failed. Check your API key."
                ) from e
            elif response.status_code == 403:
                raise APIAuthenticationError(
                    "Access denied or this feature requires a '24fire+' subscription."
                ) from e
            raise APIRequestError(f"API request failed: {e}") from e
        except requests.RequestException as e:
            raise APIRequestError(f"API request failed: {e}") from e
