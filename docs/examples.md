# Examples

This document provides various examples of using the FireAPI library.

## Basic Examples

### Server Status Check

```python
from fireapi import FireAPI

api_key = "your-api-key-here"
fire_api = FireAPI(api_key)

# Get and print server status
status = fire_api.vm.get_status()
print(f"Server Status: {status}")
```

### Server Power Management

```python
from fireapi import FireAPI
import time

api_key = "your-api-key-here"
fire_api = FireAPI(api_key)

# Start the server
fire_api.vm.start()
print("Server starting...")

# Wait for 30 seconds
time.sleep(30)

# Check status
status = fire_api.vm.get_status()
print(f"Server Status: {status}")

# Restart the server
fire_api.vm.restart()
print("Server restarting...")
```

## Async Examples

### Async Status Check

```python
import asyncio
from fireapi import AsyncFireAPI

async def check_status():
    api_key = "your-api-key-here"
    async with AsyncFireAPI(api_key) as fire_api:
        status = await fire_api.vm.get_status()
        print(f"Server Status: {status}")

asyncio.run(check_status())
```

### Async Server Management

```python
import asyncio
from fireapi import AsyncFireAPI

async def manage_server():
    api_key = "your-api-key-here"
    async with AsyncFireAPI(api_key) as fire_api:
        # Start server
        await fire_api.vm.start()
        print("Server starting...")

        # Wait for 30 seconds
        await asyncio.sleep(30)

        # Check status
        status = await fire_api.vm.get_status()
        print(f"Server Status: {status}")

asyncio.run(manage_server())
```

## Backup Management (24fire+ only)

### List and Create Backup

```python
from fireapi import FireAPI

api_key = "your-api-key-here"
fire_api = FireAPI(api_key)

# List existing backups
backups = fire_api.backup.list()
print("Existing backups:", backups)

# Create new backup
backup = fire_api.backup.create(description="Weekly backup")
print("New backup created:", backup)
```

### Async Backup Management

```python
import asyncio
from fireapi import AsyncFireAPI

async def manage_backups():
    api_key = "your-api-key-here"
    async with AsyncFireAPI(api_key) as fire_api:
        # List backups
        backups = await fire_api.backup.list()
        print("Existing backups:", backups)

        # Create backup
        backup = await fire_api.backup.create(description="Weekly backup")
        print("New backup created:", backup)

        # Delete old backups
        for old_backup in backups.data:
            if old_backup["age"] > 30:  # Delete backups older than 30 days
                await fire_api.backup.delete(backup_id=old_backup["backup_id"])
                print(f"Deleted old backup: {old_backup['backup_id']}")

asyncio.run(manage_backups())
```

## Monitoring Examples (24fire+ only)

### Check Monitoring Data

```python
from fireapi import FireAPI

api_key = "your-api-key-here"
fire_api = FireAPI(api_key)

# Get monitoring timings
timings = fire_api.monitoring.get_timings()
print("Monitoring Timings:", timings)

# Get monitoring incidences
incidences = fire_api.monitoring.get_incidences()
print("Monitoring Incidences:", incidences)
```

### Async Monitoring Check

```python
import asyncio
from fireapi import AsyncFireAPI

async def check_monitoring():
    api_key = "your-api-key-here"
    async with AsyncFireAPI(api_key) as fire_api:
        # Get monitoring data
        timings = await fire_api.monitoring.get_timings()
        incidences = await fire_api.monitoring.get_incidences()

        print("Monitoring Timings:", timings)
        print("Monitoring Incidences:", incidences)

asyncio.run(check_monitoring())
```

## Error Handling

### Basic Error Handling

```python
from fireapi import FireAPI
from fireapi.exceptions import FireAPIError

api_key = "your-api-key-here"
fire_api = FireAPI(api_key)

try:
    status = fire_api.vm.get_status()
    print(f"Server Status: {status}")
except FireAPIError as e:
    print(f"Error: {e}")
```

### Async Error Handling

```python
import asyncio
from fireapi import AsyncFireAPI
from fireapi.exceptions import FireAPIError

async def handle_errors():
    api_key = "your-api-key-here"
    try:
        async with AsyncFireAPI(api_key) as fire_api:
            status = await fire_api.vm.get_status()
            print(f"Server Status: {status}")
    except FireAPIError as e:
        print(f"Error: {e}")

asyncio.run(handle_errors())
```
