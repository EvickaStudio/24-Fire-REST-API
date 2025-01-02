from typing import Any, Optional

from ..types.backup_types import (
    BackupCreateResponse,
    BackupDeleteResponse,
    BackupListResponse,
)


class BackupResource:
    def __init__(self, client: Any) -> None:
        self.client = client

    def list(self) -> BackupListResponse:
        """List all backups.

        Returns:
            BackupListResponse: List of available backups.
        """
        response = self.client._request("backup/list")
        return BackupListResponse(**response)

    def create(self, description: Optional[str] = None) -> BackupCreateResponse:
        """Create a new backup.

        Args:
            description: Optional description for the backup (max 24 characters).
                        Allowed characters: a-z, A-Z, ä, ö, ü, Ä, Ö, Ü, ß, spaces,
                        hyphens, underscores, plus signs, hash signs, brackets,
                        dots, colons.

        Returns:
            BackupCreateResponse: Response containing the backup_id of the created backup.
        """
        data = {}
        if description is not None:
            data["description"] = description
        response = self.client._request("backup/create", method="POST", data=data)
        return BackupCreateResponse(**response)

    def delete(self, backup_id: str) -> BackupDeleteResponse:
        """Delete a backup.

        Args:
            backup_id: ID of the backup to delete.

        Returns:
            BackupDeleteResponse: Response indicating the backup was deleted.
        """
        response = self.client._request(
            "backup/delete", method="DELETE", data={"backup_id": backup_id}
        )
        return BackupDeleteResponse(**response)


class AsyncBackupResource:
    def __init__(self, client: Any) -> None:
        self.client = client

    async def list(self) -> BackupListResponse:
        """List all backups.

        Returns:
            BackupListResponse: List of available backups.
        """
        response = await self.client._request("backup/list")
        return BackupListResponse(**response)

    async def create(self, description: Optional[str] = None) -> BackupCreateResponse:
        """Create a new backup.

        Args:
            description: Optional description for the backup (max 24 characters).
                        Allowed characters: a-z, A-Z, ä, ö, ü, Ä, Ö, Ü, ß, spaces,
                        hyphens, underscores, plus signs, hash signs, brackets,
                        dots, colons.

        Returns:
            BackupCreateResponse: Response containing the backup_id of the created backup.
        """
        data = {}
        if description is not None:
            data["description"] = description
        response = await self.client._request("backup/create", method="POST", data=data)
        return BackupCreateResponse(**response)

    async def delete(self, backup_id: str) -> BackupDeleteResponse:
        """Delete a backup.

        Args:
            backup_id: ID of the backup to delete.

        Returns:
            BackupDeleteResponse: Response indicating the backup was deleted.
        """
        response = await self.client._request(
            "backup/delete", method="DELETE", data={"backup_id": backup_id}
        )
        return BackupDeleteResponse(**response)
