from typing import Any

from ..types.monitoring_types import MonitoringIncidences, MonitoringTimings


class MonitoringResource:
    def __init__(self, client: Any) -> None:
        self.client = client

    def get_timings(self) -> MonitoringTimings:
        """Get monitoring timings data.

        Returns:
            MonitoringTimings: Monitoring timing data including CPU, memory, and ping metrics.
        """
        response = self.client._request("monitoring/timings")
        return MonitoringTimings(**response)

    def get_incidences(self) -> MonitoringIncidences:
        """Get monitoring incidences data.

        Returns:
            MonitoringIncidences: Monitoring incidences data including statistics and incident history.
        """
        response = self.client._request("monitoring/incidences")
        return MonitoringIncidences(**response)


class AsyncMonitoringResource:
    def __init__(self, client: Any) -> None:
        self.client = client

    async def get_timings(self) -> MonitoringTimings:
        """Get monitoring timings data.

        Returns:
            MonitoringTimings: Monitoring timing data including CPU, memory, and ping metrics.
        """
        response = await self.client._request("monitoring/timings")
        return MonitoringTimings(**response)

    async def get_incidences(self) -> MonitoringIncidences:
        """Get monitoring incidences data.

        Returns:
            MonitoringIncidences: Monitoring incidences data including statistics and incident history.
        """
        response = await self.client._request("monitoring/incidences")
        return MonitoringIncidences(**response)
