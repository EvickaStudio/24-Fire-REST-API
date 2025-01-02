from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field


class Datacenter(BaseModel):
    name: str
    country: str
    city: str


class HostSystem(BaseModel):
    datacenter: Datacenter
    name: str
    node: str
    processor: str
    memory: str
    nvme_hard_drives: str


class OSInfo(BaseModel):
    name: str
    displayname: str


class IPAddressInfo(BaseModel):
    ip_address: str
    ip_gateway: str
    ddos_protection: Optional[str] = None
    rdns: Optional[str] = None
    requires_restart: Optional[bool] = None


class Config(BaseModel):
    cores: int
    mem: int
    disk: int
    os: OSInfo
    username: str
    password: str
    hostname: str
    network_speed: int
    backup_slots: int
    ipv4: List[IPAddressInfo]
    ipv6: List[IPAddressInfo]


class VMConfigData(BaseModel):
    hostsystem: HostSystem
    config: Config


class VMConfig(BaseModel):
    status: str
    requestID: str
    message: str
    data: VMConfigData


class UsageEntry(BaseModel):
    data: Union[str, float] = Field(
        ..., description="Can be string or float depending on status"
    )
    unit: str


class Usage(BaseModel):
    cpu: UsageEntry
    mem: UsageEntry
    nvme_storage: UsageEntry


class VMStatusData(BaseModel):
    status: str = Field(..., description="Online status of the VM (running, stopped)")
    uptime: int
    task: Optional[str] = Field(
        None, description="Current task being executed by the VM (e.g. BOOTING)"
    )
    usage: Usage


class VMStatus(BaseModel):
    status: str
    requestID: Optional[str] = None
    message: str
    data: VMStatusData


class VMPowerResponse(BaseModel):
    status: str
    requestID: str
    message: str
    data: List[Any] = Field(default_factory=list)
