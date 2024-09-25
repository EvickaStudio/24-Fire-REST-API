"""This module contains the abstract base class for FireAPI."""

from abc import ABC, abstractmethod
from typing import Dict


class BaseFireAPI(ABC):
    """Abstract base class for FireAPI."""

    def __init__(self, apiKey: str, timeout: int = 5):
        """Initializes a new FireAPI instance."""
        self.apiKey = apiKey
        self.baseUrl = "https://api.24fire.de/kvm"
        self.headers = {"X-FIRE-APIKEY": apiKey}
        self.timeout = timeout

        self.vm = self.VM(self)
        self.backup = self.Backup(self)
        self.monitoring = self.Monitoring(self)

    @abstractmethod
    def _request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Abstract method for making API requests."""
        pass

    class VM:
        """Class for VM-related methods."""

        def __init__(self, api):
            self.api = api

        def getConfig(self) -> Dict:
            """
            Retrieve the server configuration as a JSON object.

            Usage:
                >>> config = fireApi.vm.getConfig()
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
            return self.api._request("config")

        def getStatus(self) -> Dict:
            """
            Retrieve the server status as a JSON object.

            Usage:
                >>> status = fireApi.vm.getStatus()
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
            return self.api._request("status")

        def startServer(self) -> Dict:
            """
            Start the server and return the status as a JSON object.

            Usage:
                >>> response = fireApi.vm.startServer()
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
            return self.api._request("status/start", method="POST")

        def stopServer(self) -> Dict:
            """
            Stop the server and return the status as a JSON object.

            Usage:
                >>> response = fireApi.vm.stopServer()
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
            return self.api._request("status/stop", method="POST")

        def restartServer(self) -> Dict:
            """
            Restart the server and return the status as a JSON object.

            Usage:
                >>> response = fireApi.vm.restartServer()
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
            return self.api._request("status/restart", method="POST")

    class Backup:
        """Class for Backup-related methods."""

        def __init__(self, api):
            self.api = api

        def deleteBackup(self, backup_id: str) -> Dict:
            """
            Delete a backup.

            Note: This operation is exclusive to '24fire+' subscribers.

            Args:
                backup_id (str): The ID of the backup to delete.

            Usage:
                >>> response = fireApi.backup.deleteBackup("backup_id")
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
            return self.api._request(
                f"backup/delete?backup_id={backup_id}", method="DELETE"
            )

        def createBackup(self, description: str) -> Dict:
            """
            Create a backup with a description.

            Note: This operation is exclusive to '24fire+' subscribers.

            Args:
                description (str): Description of the backup.

            Usage:
                >>> response = fireApi.backup.createBackup("Backup description")
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
            return self.api._request(
                "backup/create", method="POST", data={"description": description}
            )

        def listBackup(self) -> Dict:
            """
            List all backups.

            Note: This operation is exclusive to '24fire+' subscribers.

            Usage:
                >>> backups = fireApi.backup.listBackup()
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
            return self.api._request("backup/list")

    class Monitoring:
        """Class for Monitoring-related methods."""

        def __init__(self, api):
            self.api = api

        def timings(self) -> Dict:
            """
            Retrieve monitoring timings.

            Note: This operation is exclusive to '24fire+' subscribers.

            Usage:
                >>> timings = fireApi.monitoring.timings()
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
            return self.api._request("monitoring/timings")

        def incidences(self) -> Dict:
            """
            Retrieve monitoring incidences.

            Note: This operation is exclusive to '24fire+' subscribers.

            Usage:
                >>> incidences = fireApi.monitoring.incidences()
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
            return self.api._request("monitoring/incidences")
