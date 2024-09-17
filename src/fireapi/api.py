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

        Example Response:
        {
            "status": "success",
            "requestID": "9a220700-00c4-42f7-bc8c-9487f09ec72c",
            "message": "VM config retrieved successfully",
            "data": {
                "hostsystem": {
                    "datacenter": {
                        "name": "SkyLink Data Center BV",
                        "country": "Niederlande",
                        "city": "Eygelshoven"
                    },
                    "name": "nl_xeon",
                    "node": "XEON 04",
                    "processor": "Intel(R) Xeon(R) CPU E5-2690 v2 @ 3.00GHz",
                    "memory": "DDR3 Synchronous Registered (Buffered) 1600 MHz",
                    "nvme_hard_drives": "Samsung SSD PM9A1"
                },
                "config": {
                    "cores": 5,
                    "mem": 41984,
                    "disk": 70,
                    "os": {
                        "name": "debian_11",
                        "displayname": "Debian 11"
                    },
                    "username": "root",
                    "password": "xxxxxxxxxx",
                    "hostname": "KVM",
                    "network_speed": 2000,
                    "backup_slots": 2,
                    "ipv4": [
                        {
                            "ip_address": "88.151.xxx.xxx",
                            "ip_gateway": "88.151.xxx.xxx",
                            "ddos_protection": "arbor",
                            "rdns": "24fire.de"
                        }
                    ],
                    "ipv6": [
                        {
                            "ip_address": "2a12:8641:xxxx:xxxx::",
                            "ip_gateway": "2a12:8641:xxxx::xxxx",
                            "requires_restart": false
                        }
                    ]
                }
            }
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "1775ed52-4eec-48fa-8880-e7285e59ef1a",
            "message": "VM status retrieved successfully",
            "data": {
                "status": "running",
                "uptime": 545,
                "task": null,
                "usage": {
                    "cpu": {
                        "data": "0.000",
                        "unit": "%"
                    },
                    "mem": {
                        "data": "0.659",
                        "unit": "MB"
                    },
                    "nvme_storage": {
                        "data": 1.7,
                        "unit": "GB"
                    }
                }
            }
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "6220a191-fe11-4d56-a67d-2686b5020505",
            "message": "VM power command sent",
            "data": []
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "237f18b1-b1f7-454c-b59a-7d971878dc49",
            "message": "VM power command sent",
            "data": []
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "237f18b1-b1f7-454c-b59a-7d971878dc49",
            "message": "VM power command sent",
            "data": []
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "d27f2df2-c7f4-4a42-9152-c24d5efdf118",
            "message": "VM backup deleted",
            "data": null
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "07696208-1c38-4a93-8f44-b9557bae55e2",
            "message": "VM backup task started",
            "data": {
                "backup_id": "4bd60b8f-d875-4fb9-88bc-6d930d9ff011"
            }
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "0b6c6067-475e-4000-b2e9-73993287c6c2",
            "message": "VM backups are listed below",
            "data": [
                {
                    "backup_id": "f31ee183-7037-4e60-a37d-0f7406fd32d7",
                    "backup_os": "debian_11",
                    "backup_description": "Durch eine Automatisierung erstellt",
                    "size": 2200,
                    "created": "2024-01-25T14:02:14.000Z",
                    "status": "finished"
                },
                {
                    "backup_id": "4bd60b8f-d875-4fb9-88bc-6d930d9ff011",
                    "backup_os": "debian_11",
                    "backup_description": "Durch 24fire REST API erstellt",
                    "size": 2200,
                    "created": "2024-01-25T16:49:11.000Z",
                    "status": "finished"
                }
            ]
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "40d548f5-7edc-4146-950c-dd01c2486a82",
            "message": "monitoring timings are listed below",
            "data": {
                "timings": [
                    {
                        "date": "2024-01-03T22:34:02.000Z",
                        "cpu": "0.481",
                        "mem": "1.261",
                        "ping": 19
                    },
                    {
                        "date": "2024-01-03T22:44:02.000Z",
                        "cpu": "0.461",
                        "mem": "1.261",
                        "ping": 18
                    }
                ]
            }
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "cf1a55c7-70e2-4c15-acd1-678291ca5737",
            "message": "monitoring incidences are listed below",
            "data": {
                "statistic": {
                    "LAST_24_HOURS": {
                        "downtime": 0,
                        "availability": 100,
                        "incidences": 0,
                        "longest_incidence": 0,
                        "average_incidence": 0
                    },
                    "LAST_7_DAYS": {
                        "downtime": 0,
                        "availability": 100,
                        "incidences": 0,
                        "longest_incidence": 0,
                        "average_incidence": 0
                    },
                    "LAST_14_DAYS": {
                        "downtime": 1422,
                        "availability": 97.1787,
                        "incidences": 4,
                        "longest_incidence": 1402,
                        "average_incidence": 355.49
                    },
                    "LAST_30_DAYS": {
                        "downtime": 2475,
                        "availability": 97.7088,
                        "incidences": 17,
                        "longest_incidence": 1402,
                        "average_incidence": 145.56
                    },
                    "LAST_90_DAYS": {
                        "downtime": 2475,
                        "availability": 99.2363,
                        "incidences": 17,
                        "longest_incidence": 1402,
                        "average_incidence": 145.56
                    },
                    "LAST_180_DAYS": {
                        "downtime": 2475,
                        "availability": 99.6181,
                        "incidences": 17,
                        "longest_incidence": 1402,
                        "average_incidence": 145.56
                    }
                },
                "incidences": [
                    {
                        "start": "2024-01-16T13:46:02.000Z",
                        "end": "2024-01-17T13:08:01.000Z",
                        "downtime": 1402,
                        "type": "PING_TIMEOUT"
                    },
                    {
                        "start": "2024-01-14T19:44:02.000Z",
                        "end": "2024-01-14T19:53:01.000Z",
                        "downtime": 9,
                        "type": "VM_STOPPED"
                    },
                    {
                        "start": "2024-01-14T19:32:01.000Z",
                        "end": "2024-01-14T19:41:01.000Z",
                        "downtime": 9,
                        "type": "VM_STOPPED"
                    },
                    {
                        "start": "2024-01-10T17:18:02.000Z",
                        "end": "2024-01-10T17:20:01.000Z",
                        "downtime": 2,
                        "type": "PING_TIMEOUT"
                    },
                    {
                        "start": "2024-01-07T22:27:02.000Z",
                        "end": "2024-01-07T23:12:00.000Z",
                        "downtime": 45,
                        "type": "PING_TIMEOUT"
                    },
                    {
                        "start": "2024-01-07T19:25:01.000Z",
                        "end": "2024-01-07T19:27:00.000Z",
                        "downtime": 2,
                        "type": "PING_TIMEOUT"
                    }
                ]
            }
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "0b0...",
            "message": "VM config retrieved successfully",
            "data": {
                "hostsystem": {
                    "datacenter": {
                        "name": "NTT FRA1 Data Center",
                        "country": "Deutschland",
                        "city": "Frankfurt am Main"
                    },
                    "name": "de_epyc",
                    "node": "EPYC 02",
                    "processor": "AMD EPYC 7443P",
                    "memory": "Samsung registered DDR4 ECC 3200 MHz",
                    "nvme_hard_drives": "Samsung NVMe SSD PM9A3"
                },
                "config": {
                    "cores": 4,
                    "mem": 12288,
                    "disk": 50,
                    "storage": null,
                    "traffic_limit": 1000,
                    "os": {
                        "name": "debian_11",
                        "displayname": "Debian 11"
                    },
                    "iso": null,
                    "username": "",
                    "password": "",
                    "password_enabled": true,
                    "hostname": "24fire",
                    "network_speed": 1000,
                    "backup_slots": 2,
                    "ipv4": [
                        {
                            "ip_address": "",
                            "ip_gateway": "",
                            "ddos_protection": "inhouse_shield",
                            "rdns": "24fire.de"
                        }
                    ],
                    "ipv6": [
                        {
                            "ip_address": "",
                            "ip_gateway": "",
                            "requires_restart": false
                        }
                    ],
                    "monitoring": {
                        "enabled": true,
                        "port": 22
                    }
                }
            }
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "1775ed52-4eec-48fa-8880-e7285e59ef1a",
            "message": "VM status retrieved successfully",
            "data": {
                "status": "running",
                "uptime": 545,
                "task": null,
                "usage": {
                    "cpu": {
                        "data": "0.000",
                        "unit": "%"
                    },
                    "mem": {
                        "data": "0.659",
                        "unit": "MB"
                    },
                    "nvme_storage": {
                        "data": 1.7,
                        "unit": "GB"
                    }
                }
            }
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "6220a191-fe11-4d56-a67d-2686b5020505",
            "message": "VM power command sent",
            "data": []
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "237f18b1-b1f7-454c-b59a-7d971878dc49",
            "message": "VM power command sent",
            "data": []
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

        Example Response:
        {
            "status": "success",
            "requestID": "237f18b1-b1f7-454c-b59a-7d971878dc49",
            "message": "VM power command sent",
            "data": []
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "d27f2df2-c7f4-4a42-9152-c24d5efdf118",
            "message": "VM backup deleted",
            "data": null
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "07696208-1c38-4a93-8f44-b9557bae55e2",
            "message": "VM backup task started",
            "data": {
                "backup_id": "4bd60b8f-d875-4fb9-88bc-6d930d9ff011"
            }
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "0b6c6067-475e-4000-b2e9-73993287c6c2",
            "message": "VM backups are listed below",
            "data": [
                {
                    "backup_id": "f31ee183-7037-4e60-a37d-0f7406fd32d7",
                    "backup_os": "debian_11",
                    "backup_description": "Durch eine Automatisierung erstellt",
                    "size": 2200,
                    "created": "2024-01-25T14:02:14.000Z",
                    "status": "finished"
                },
                {
                    "backup_id": "4bd60b8f-d875-4fb9-88bc-6d930d9ff011",
                    "backup_os": "debian_11",
                    "backup_description": "Durch 24fire REST API erstellt",
                    "size": 2200,
                    "created": "2024-01-25T16:49:11.000Z",
                    "status": "finished"
                }
            ]
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "40d548f5-7edc-4146-950c-dd01c2486a82",
            "message": "monitoring timings are listed below",
            "data": {
                "timings": [
                    {
                        "date": "2024-01-03T22:34:02.000Z",
                        "cpu": "0.481",
                        "mem": "1.261",
                        "ping": 19
                    },
                    {
                        "date": "2024-01-03T22:44:02.000Z",
                        "cpu": "0.461",
                        "mem": "1.261",
                        "ping": 18
                    }
                ]
            }
        }
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

        Example Response:
        {
            "status": "success",
            "requestID": "cf1a55c7-70e2-4c15-acd1-678291ca5737",
            "message": "monitoring incidences are listed below",
            "data": {
                "statistic": {
                    "LAST_24_HOURS": {
                        "downtime": 0,
                        "availability": 100,
                        "incidences": 0,
                        "longest_incidence": 0,
                        "average_incidence": 0
                    },
                    "LAST_7_DAYS": {
                        "downtime": 0,
                        "availability": 100,
                        "incidences": 0,
                        "longest_incidence": 0,
                        "average_incidence": 0
                    },
                    "LAST_14_DAYS": {
                        "downtime": 1422,
                        "availability": 97.1787,
                        "incidences": 4,
                        "longest_incidence": 1402,
                        "average_incidence": 355.49
                    },
                    "LAST_30_DAYS": {
                        "downtime": 2475,
                        "availability": 97.7088,
                        "incidences": 17,
                        "longest_incidence": 1402,
                        "average_incidence": 145.56
                    },
                    "LAST_90_DAYS": {
                        "downtime": 2475,
                        "availability": 99.2363,
                        "incidences": 17,
                        "longest_incidence": 1402,
                        "average_incidence": 145.56
                    },
                    "LAST_180_DAYS": {
                        "downtime": 2475,
                        "availability": 99.6181,
                        "incidences": 17,
                        "longest_incidence": 1402,
                        "average_incidence": 145.56
                    }
                },
                "incidences": [
                    {
                        "start": "2024-01-16T13:46:02.000Z",
                        "end": "2024-01-17T13:08:01.000Z",
                        "downtime": 1402,
                        "type": "PING_TIMEOUT"
                    },
                    {
                        "start": "2024-01-14T19:44:02.000Z",
                        "end": "2024-01-14T19:53:01.000Z",
                        "downtime": 9,
                        "type": "VM_STOPPED"
                    },
                    {
                        "start": "2024-01-14T19:32:01.000Z",
                        "end": "2024-01-14T19:41:01.000Z",
                        "downtime": 9,
                        "type": "VM_STOPPED"
                    },
                    {
                        "start": "2024-01-10T17:18:02.000Z",
                        "end": "2024-01-10T17:20:01.000Z",
                        "downtime": 2,
                        "type": "PING_TIMEOUT"
                    },
                    {
                        "start": "2024-01-07T22:27:02.000Z",
                        "end": "2024-01-07T23:12:00.000Z",
                        "downtime": 45,
                        "type": "PING_TIMEOUT"
                    },
                    {
                        "start": "2024-01-07T19:25:01.000Z",
                        "end": "2024-01-07T19:27:00.000Z",
                        "downtime": 2,
                        "type": "PING_TIMEOUT"
                    }
                ]
            }
        }
        """
        return await self._request("monitoring/incidences")
