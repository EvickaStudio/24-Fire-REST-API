# Advanced Usage

This guide covers advanced usage patterns and best practices for the FireAPI library.

## Custom Session Management

### Custom HTTP Session

You can customize the HTTP session used by the client:

```python
import requests
from fireapi import FireAPI

# Create a custom session
session = requests.Session()
session.headers.update({
    "User-Agent": "MyCustomApp/1.0",
    "Accept": "application/json"
})

# Pass the session to the client
api_key = "your-api-key-here"
fire_api = FireAPI(api_key, session=session)
```

### Custom Async Session

Similarly for async clients:

```python
import aiohttp
from fireapi import AsyncFireAPI

async def custom_session():
    # Create custom session with timeout
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        fire_api = AsyncFireAPI(api_key, session=session)
        status = await fire_api.vm.get_status()
        print(f"Status: {status}")
```

## Retry Handling

### Implementing Retries

```python
from fireapi import FireAPI
from fireapi.exceptions import FireAPIError
import time

def get_status_with_retry(api_key: str, max_retries: int = 3, delay: float = 1.0):
    fire_api = FireAPI(api_key)

    for attempt in range(max_retries):
        try:
            return fire_api.vm.get_status()
        except FireAPIError as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay * (attempt + 1))  # Exponential backoff
```

### Async Retry Implementation

```python
import asyncio
from fireapi import AsyncFireAPI
from fireapi.exceptions import FireAPIError

async def get_status_with_retry(api_key: str, max_retries: int = 3, delay: float = 1.0):
    async with AsyncFireAPI(api_key) as fire_api:
        for attempt in range(max_retries):
            try:
                return await fire_api.vm.get_status()
            except FireAPIError as e:
                if attempt == max_retries - 1:
                    raise
                print(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(delay * (attempt + 1))
```

## Batch Operations

### Managing Multiple Backups

```python
from fireapi import FireAPI
from typing import List
import time

def batch_create_backups(api_key: str, descriptions: List[str], delay: float = 5.0):
    fire_api = FireAPI(api_key)
    results = []

    for desc in descriptions:
        try:
            backup = fire_api.backup.create(description=desc)
            results.append({"success": True, "backup": backup})
        except FireAPIError as e:
            results.append({"success": False, "error": str(e)})
        time.sleep(delay)  # Avoid rate limiting

    return results
```

### Async Batch Operations

```python
from fireapi import AsyncFireAPI
from typing import List
import asyncio

async def batch_create_backups(api_key: str, descriptions: List[str]):
    async with AsyncFireAPI(api_key) as fire_api:
        tasks = []
        for desc in descriptions:
            # Create backup tasks with delay to avoid rate limiting
            task = asyncio.create_task(
                fire_api.backup.create(description=desc)
            )
            tasks.append(task)
            await asyncio.sleep(5)  # Delay between creations

        results = []
        for task in tasks:
            try:
                result = await task
                results.append({"success": True, "backup": result})
            except FireAPIError as e:
                results.append({"success": False, "error": str(e)})

        return results
```

## Advanced Error Handling

### Custom Error Handler

```python
from fireapi import FireAPI
from fireapi.exceptions import FireAPIError
import logging

class CustomErrorHandler:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def handle_error(self, error: FireAPIError, context: dict):
        self.logger.error(f"API Error: {error}")
        self.logger.debug(f"Context: {context}")

        if error.status_code == 429:  # Rate limit
            self.logger.warning("Rate limit reached")
        elif error.status_code >= 500:  # Server error
            self.logger.critical("Server error occurred")

        # Re-raise the error for the caller to handle
        raise error

# Usage
handler = CustomErrorHandler()
fire_api = FireAPI(api_key)

try:
    status = fire_api.vm.get_status()
except FireAPIError as e:
    handler.handle_error(e, {"operation": "get_status"})
```

## Rate Limiting

### Rate Limit Handler

```python
import time
from fireapi import FireAPI
from fireapi.exceptions import FireAPIError

class RateLimitHandler:
    def __init__(self, max_requests: int = 60, time_window: float = 60.0):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []

    def wait_if_needed(self):
        now = time.time()
        # Remove old requests
        self.requests = [t for t in self.requests if now - t < self.time_window]

        if len(self.requests) >= self.max_requests:
            # Wait until oldest request expires
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.requests = self.requests[1:]

        self.requests.append(now)

# Usage
rate_limiter = RateLimitHandler(max_requests=60, time_window=60.0)
fire_api = FireAPI(api_key)

for _ in range(100):
    rate_limiter.wait_if_needed()
    try:
        status = fire_api.vm.get_status()
        print(status)
    except FireAPIError as e:
        print(f"Error: {e}")
```

## Async Context Managers

### Custom Async Context Manager

```python
from fireapi import AsyncFireAPI
from types import TracebackType
from typing import Optional, Type

class AsyncFireAPIManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client: Optional[AsyncFireAPI] = None

    async def __aenter__(self) -> AsyncFireAPI:
        self.client = AsyncFireAPI(self.api_key)
        return self.client

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        if self.client:
            await self.client.close()

# Usage
async def main():
    async with AsyncFireAPIManager("your-api-key") as fire_api:
        status = await fire_api.vm.get_status()
        print(status)
```
