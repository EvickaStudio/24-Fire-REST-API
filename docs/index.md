# FireAPI Documentation

Welcome to the FireAPI documentation! This library provides a Python interface to the 24Fire REST API, allowing you to manage your KVM servers programmatically.

## Documentation Contents

### Core Documentation
- [Getting Started](getting_started.md) - Quick start guide and basic usage
- [API Reference](api_reference.md) - Detailed API documentation
- [Examples](examples.md) - Code examples for common use cases
- [Advanced Usage](advanced_usage.md) - Advanced features and patterns
- [Best Practices](best_practices.md) - Recommended practices and patterns

### Additional Resources
- [GitHub Repository](https://github.com/EvickaStudio/24-Fire-REST-API)
- [24Fire API Documentation](https://apidocs.24fire.de/)
- [PyPI Package](https://pypi.org/project/fireapi/)

## Quick Links

### Installation
```bash
pip install fireapi
```

### Basic Usage
```python
from fireapi import FireAPI

api_key = "your-api-key-here"
fire_api = FireAPI(api_key)

# Get server status
status = fire_api.vm.get_status()
print(f"Server Status: {status}")
```

### Async Usage
```python
import asyncio
from fireapi import AsyncFireAPI

async def main():
    async with AsyncFireAPI("your-api-key-here") as fire_api:
        status = await fire_api.vm.get_status()
        print(f"Server Status: {status}")

asyncio.run(main())
```

## Features

- **Server Management**
  - Get server configuration
  - Get server status
  - Start, stop, and restart server

- **Backup Management** (24fire+ only)
  - List backups
  - Create backups
  - Delete backups

- **Monitoring** (24fire+ only)
  - Get monitoring timings
  - Get monitoring incidences

## Support

If you encounter any issues or have questions:

1. Check the [documentation](https://github.com/EvickaStudio/24-Fire-REST-API/tree/main/docs)
2. Open an [issue on GitHub](https://github.com/EvickaStudio/24-Fire-REST-API/issues)
3. Contact [24Fire Support](https://24fire.de/support) for API-specific questions

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/EvickaStudio/24-Fire-REST-API/blob/main/CONTRIBUTING.md) for details.
