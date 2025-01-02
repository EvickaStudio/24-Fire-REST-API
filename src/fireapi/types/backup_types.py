from typing import List

from pydantic import BaseModel, Field


class BackupItem(BaseModel):
    backup_id: str
    backup_os: str
    backup_description: str
    size: int
    created: str
    status: str = Field(..., description="Status of the backup")


class BackupListResponse(BaseModel):
    status: str
    requestID: str
    message: str
    data: List[BackupItem]


class BackupCreateResponse(BaseModel):
    status: str
    requestID: str
    message: str
    data: dict = Field(..., description="Contains backup_id of the created backup")


class BackupDeleteResponse(BaseModel):
    status: str
    requestID: str
    message: str
    data: None = None
