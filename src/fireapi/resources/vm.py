from typing import Any

from ..types.vm_types import VMConfig, VMPowerResponse, VMStatus


class VMResource:
    def __init__(self, client: Any) -> None:
        self.client = client

    def get_config(self) -> VMConfig:
        """Get the VM configuration.

        Returns:
            VMConfig: The VM configuration details.
        """
        response = self.client._request("config")
        return VMConfig(**response)

    def get_status(self) -> VMStatus:
        """Get the current VM status.

        Returns:
            VMStatus: The current VM status including uptime and resource usage.
        """
        response = self.client._request("status")
        return VMStatus(**response)

    def start(self) -> VMPowerResponse:
        """Start the VM.

        Returns:
            VMPowerResponse: The response indicating the power command was sent.
        """
        response = self.client._request("status/start", method="POST")
        return VMPowerResponse(**response)

    def stop(self) -> VMPowerResponse:
        """Stop the VM.

        Returns:
            VMPowerResponse: The response indicating the power command was sent.
        """
        response = self.client._request("status/stop", method="POST")
        return VMPowerResponse(**response)

    def restart(self) -> VMPowerResponse:
        """Restart the VM.

        Returns:
            VMPowerResponse: The response indicating the power command was sent.
        """
        response = self.client._request("status/restart", method="POST")
        return VMPowerResponse(**response)


class AsyncVMResource:
    def __init__(self, client: Any) -> None:
        self.client = client

    async def get_config(self) -> VMConfig:
        """Get the VM configuration.

        Returns:
            VMConfig: The VM configuration details.
        """
        response = await self.client._request("config")
        return VMConfig(**response)

    async def get_status(self) -> VMStatus:
        """Get the current VM status.

        Returns:
            VMStatus: The current VM status including uptime and resource usage.
        """
        response = await self.client._request("status")
        return VMStatus(**response)

    async def start(self) -> VMPowerResponse:
        """Start the VM.

        Returns:
            VMPowerResponse: The response indicating the power command was sent.
        """
        response = await self.client._request("status/start", method="POST")
        return VMPowerResponse(**response)

    async def stop(self) -> VMPowerResponse:
        """Stop the VM.

        Returns:
            VMPowerResponse: The response indicating the power command was sent.
        """
        response = await self.client._request("status/stop", method="POST")
        return VMPowerResponse(**response)

    async def restart(self) -> VMPowerResponse:
        """Restart the VM.

        Returns:
            VMPowerResponse: The response indicating the power command was sent.
        """
        response = await self.client._request("status/restart", method="POST")
        return VMPowerResponse(**response)
