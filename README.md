# FireAPI

[![PyPI version](https://badge.fury.io/py/fireapi.svg)](https://badge.fury.io/py/fireapi)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/EvickaStudio/24-Fire-REST-API/blob/main/LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

FireAPI is a Python library that serves as a wrapper for the 24Fire REST API. It allows you to perform basic operations on a KVM server using a private API key. The library provides the following functionalities:

- Get server configuration
- Get server status
- Start server
- Stop server
- Restart server

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

## Documentation

For more information on the 24Fire REST API, refer to the [original documentation](https://documenter.getpostman.com/view/18955936/2s93zB6hJu).
