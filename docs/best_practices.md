# Best Practices

This guide outlines best practices for using the FireAPI library effectively and safely.

## API Key Management

### Environment Variables

Store your API key in environment variables rather than hardcoding it:

```python
import os
from fireapi import FireAPI

api_key = os.getenv("FIRE_API_KEY")
if not api_key:
    raise ValueError("FIRE_API_KEY environment variable not set")

fire_api = FireAPI(api_key)
```

### Configuration Files

For applications, use a configuration file:

```python
import configparser
from fireapi import FireAPI

config = configparser.ConfigParser()
config.read("config.ini")

api_key = config.get("fireapi", "api_key")
fire_api = FireAPI(api_key)
```

## Resource Management

### Using Context Managers

Always use context managers with async clients to ensure proper cleanup:

```python
async with AsyncFireAPI(api_key) as fire_api:
    status = await fire_api.vm.get_status()
```

### Session Reuse

Reuse sessions for multiple operations:

```python
import requests
from fireapi import FireAPI

with requests.Session() as session:
    fire_api = FireAPI(api_key, session=session)

    # Multiple operations using the same session
    config = fire_api.vm.get_config()
    status = fire_api.vm.get_status()
```

## Error Handling

### Comprehensive Error Handling

Always handle potential errors:

```python
from fireapi import FireAPI, FireAPIError
import logging

logger = logging.getLogger(__name__)

try:
    fire_api = FireAPI(api_key)
    status = fire_api.vm.get_status()
except FireAPIError as e:
    logger.error(f"API Error: {e}")
    # Handle specific error cases
    if e.status_code == 401:
        logger.error("Invalid API key")
    elif e.status_code == 429:
        logger.warning("Rate limit exceeded")
except Exception as e:
    logger.exception("Unexpected error")
```

### Graceful Degradation

Implement fallback behavior for non-critical operations:

```python
def get_monitoring_data(fire_api):
    try:
        return fire_api.monitoring.get_timings()
    except FireAPIError as e:
        if e.status_code == 404:
            # Monitoring might not be available (non-24fire+ user)
            return None
        raise  # Re-raise other errors
```

## Performance Optimization

### Batch Operations

Group related operations to minimize API calls:

```python
async def process_backups(fire_api):
    # Get all backups in one call
    backups = await fire_api.backup.list()

    # Process in memory
    old_backups = [
        b for b in backups.data
        if b["age"] > 30
    ]

    # Batch delete old backups
    for backup in old_backups:
        await fire_api.backup.delete(backup["backup_id"])
```

### Caching

Cache responses when appropriate:

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedFireAPI:
    def __init__(self, api_key: str):
        self.api = FireAPI(api_key)
        self._cache_time = None
        self._cached_config = None

    def get_config(self, max_age_minutes: int = 5):
        now = datetime.now()
        if (not self._cached_config or
            not self._cache_time or
            now - self._cache_time > timedelta(minutes=max_age_minutes)):
            self._cached_config = self.api.vm.get_config()
            self._cache_time = now
        return self._cached_config
```

## Rate Limiting

### Implement Rate Limiting

Use rate limiting to avoid hitting API limits:

```python
import time
from functools import wraps

def rate_limit(calls: int, period: float):
    def decorator(func):
        last_reset = time.time()
        calls_made = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_reset, calls_made

            now = time.time()
            if now - last_reset >= period:
                calls_made = 0
                last_reset = now

            if calls_made >= calls:
                sleep_time = period - (now - last_reset)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                calls_made = 0
                last_reset = time.time()

            calls_made += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@rate_limit(calls=60, period=60.0)
def get_server_status(fire_api):
    return fire_api.vm.get_status()
```

## Testing

### Mock API Responses

Use mocking for tests:

```python
from unittest.mock import patch
import pytest

def test_server_status():
    mock_response = {
        "status": "running",
        "uptime": 3600
    }

    with patch("fireapi.FireAPI.vm.get_status") as mock_status:
        mock_status.return_value = mock_response

        fire_api = FireAPI("test-key")
        status = fire_api.vm.get_status()

        assert status["status"] == "running"
        assert status["uptime"] == 3600
```

### Async Testing

Use pytest-asyncio for testing async code:

```python
import pytest
import asyncio
from fireapi import AsyncFireAPI

@pytest.mark.asyncio
async def test_async_status():
    async with AsyncFireAPI("test-key") as fire_api:
        with patch.object(fire_api.vm, "get_status") as mock_status:
            mock_status.return_value = {"status": "running"}

            status = await fire_api.vm.get_status()
            assert status["status"] == "running"
```

## Logging

### Structured Logging

Implement comprehensive logging:

```python
import logging
import json

class FireAPILogger:
    def __init__(self):
        self.logger = logging.getLogger("fireapi")
        self.logger.setLevel(logging.INFO)

        # Add JSON handler
        handler = logging.FileHandler("fireapi.log")
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(message)s")
        )
        self.logger.addHandler(handler)

    def log_request(self, method: str, endpoint: str, **kwargs):
        self.logger.info(
            json.dumps({
                "type": "request",
                "method": method,
                "endpoint": endpoint,
                **kwargs
            })
        )

    def log_response(self, status_code: int, response_time: float, **kwargs):
        self.logger.info(
            json.dumps({
                "type": "response",
                "status_code": status_code,
                "response_time_ms": response_time * 1000,
                **kwargs
            })
        )

# Usage
logger = FireAPILogger()
logger.log_request("GET", "/vm/status")
```
