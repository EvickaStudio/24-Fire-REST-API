# Getting Started with FireAPI

This guide will help you get started with FireAPI, a Python client library for the 24Fire REST API.

## Prerequisites

- Python 3.7 or higher
- A 24Fire account with API access
- Your API key from the 24Fire dashboard

## Installation

### Standard Installation

Install FireAPI using pip:

```bash
pip install fireapi
```

### Development Installation

For the latest development version:

```bash
pip install --pre fireapi
```

## Quick Start

### Basic Usage

```python
from fireapi import FireAPI

# Initialize the client
api_key = "your-api-key-here"
fire_api = FireAPI(api_key)

# Get server configuration
config = fire_api.vm.get_config()
print(f"Server Configuration: {config}")

# Check server status
status = fire_api.vm.get_status()
print(f"Server Status: {status}")
```

### Async Usage

```python
import asyncio
from fireapi import AsyncFireAPI

async def main():
    api_key = "your-api-key-here"
    async with AsyncFireAPI(api_key) as fire_api:
        config = await fire_api.vm.get_config()
        print(f"Server Configuration: {config}")

asyncio.run(main())
```

## Next Steps

- Check out the [API Reference](api_reference.md) for detailed information about available methods
- See [Examples](examples.md) for more usage examples
- Read about [Advanced Usage](advanced_usage.md) for more complex scenarios
- Review [Best Practices](best_practices.md) for optimal usage
