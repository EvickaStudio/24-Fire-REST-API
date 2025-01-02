# API Reference

This document provides detailed information about all available classes and methods in the FireAPI library.

## Client Classes

### FireAPI

The main synchronous client class.

```python
class FireAPI:
    def __init__(self, api_key: str):
        """Initialize the FireAPI client.

        Args:
            api_key (str): Your 24Fire API key
        """
```

### AsyncFireAPI

The asynchronous client class.

```python
class AsyncFireAPI:
    def __init__(self, api_key: str):
        """Initialize the AsyncFireAPI client.

        Args:
            api_key (str): Your 24Fire API key
        """
```

## Resources

### VM Resource

Methods for managing virtual machines.

#### Synchronous Methods

```python
def get_config(self) -> VMConfig:
    """Get the VM configuration."""

def get_status(self) -> VMStatus:
    """Get the current VM status."""

def start(self) -> VMResponse:
    """Start the VM."""

def stop(self) -> VMResponse:
    """Stop the VM."""

def restart(self) -> VMResponse:
    """Restart the VM."""
```

#### Asynchronous Methods

```python
async def get_config(self) -> VMConfig:
    """Get the VM configuration."""

async def get_status(self) -> VMStatus:
    """Get the current VM status."""

async def start(self) -> VMResponse:
    """Start the VM."""

async def stop(self) -> VMResponse:
    """Stop the VM."""

async def restart(self) -> VMResponse:
    """Restart the VM."""
```

### Backup Resource (24fire+ only)

Methods for managing backups.

#### Synchronous Methods

```python
def list(self) -> BackupListResponse:
    """List all available backups."""

def create(self, description: Optional[str] = None) -> BackupCreateResponse:
    """Create a new backup.

    Args:
        description (str, optional): Description for the backup
    """

def delete(self, backup_id: str) -> BackupDeleteResponse:
    """Delete a backup.

    Args:
        backup_id (str): ID of the backup to delete
    """
```

#### Asynchronous Methods

```python
async def list(self) -> BackupListResponse:
    """List all available backups."""

async def create(self, description: Optional[str] = None) -> BackupCreateResponse:
    """Create a new backup.

    Args:
        description (str, optional): Description for the backup
    """

async def delete(self, backup_id: str) -> BackupDeleteResponse:
    """Delete a backup.

    Args:
        backup_id (str): ID of the backup to delete
    """
```

### Monitoring Resource (24fire+ only)

Methods for retrieving monitoring data.

#### Synchronous Methods

```python
def get_timings(self) -> MonitoringTimings:
    """Get monitoring timing data."""

def get_incidences(self) -> MonitoringIncidences:
    """Get monitoring incidence data."""
```

#### Asynchronous Methods

```python
async def get_timings(self) -> MonitoringTimings:
    """Get monitoring timing data."""

async def get_incidences(self) -> MonitoringIncidences:
    """Get monitoring incidence data."""
```

## Response Types

### VM Types

```python
class VMConfig(BaseModel):
    """VM configuration response."""
    # Configuration fields

class VMStatus(BaseModel):
    """VM status response."""
    # Status fields

class VMResponse(BaseModel):
    """Generic VM operation response."""
    # Response fields
```

### Backup Types

```python
class BackupListResponse(BaseModel):
    """Response for listing backups."""
    # List response fields

class BackupCreateResponse(BaseModel):
    """Response for creating a backup."""
    # Create response fields

class BackupDeleteResponse(BaseModel):
    """Response for deleting a backup."""
    # Delete response fields
```

### Monitoring Types

```python
class MonitoringTimings(BaseModel):
    """Response for monitoring timings."""
    # Timing fields

class MonitoringIncidences(BaseModel):
    """Response for monitoring incidences."""
    # Incidence fields
```
