# FireAPI

[![PyPI version](https://badge.fury.io/py/fireapi.svg)](https://badge.fury.io/py/fireapi)
[![Downloads](https://pepy.tech/badge/fireapi)](https://pepy.tech/project/fireapi)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fireapi.svg)](https://pypi.org/project/fireapi/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

FireAPI is a Python library that serves as a wrapper for the 24Fire REST API. It allows you to perform basic operations on a KVM server using a private API key. The library provides the following functionalities:

- Get server configuration
- Get server status
- Start server
- Stop server
- Restart server
- Async Support

## Installation

To install FireAPI, use pip:

```bash
pip install fireapi
```

Alternatively, you can build and install the package manually:

```bash
# Clone the repository
git clone https://github.com/EvickaStudio/24-Fire-REST-API.git
# Change directory
cd 24-Fire-REST-API
# Build the package
python setup.py sdist bdist_wheel
# Install the package
pip install ./
```

Then install the package using pip:

## Usage

To get started, import the `FireAPI` class from the `fireapi` package and instantiate it using your API key:

```python
from fireapi import FireAPI

API_KEY = "your-api-key-here"
fire_api = FireAPI(API_KEY)
```

Once the instance is created, you can interact with the 24Fire REST API using the provided methods:

```python
# Get server configuration
config = fire_api.get_config()
print(config)

# Get server status
status = fire_api.get_status()
print(status)

# Start server
start = fire_api.start_server()
print(start)

# Stop server
stop = fire_api.stop_server()
print(stop)

# Restart server
restart = fire_api.restart_server()
print(restart)
```

When using the `async` methods, you can use the `await` keyword to wait for the response:

```python
import asyncio
from fireapi import AsyncFireAPI

async def main():
    API_KEY = "your-api-key-here"
    try:
        fire_api = AsyncFireAPI(API_KEY)
        # Get server configuration
        config = await fire_api.get_config()
        print(config)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

For more information on the 24Fire REST API, refer to the [original documentation](https://apidocs.24fire.de/).
