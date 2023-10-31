# FireAPI

FireAPI is a Python library designed to serve as a wrapper for the 24Fire REST API. It enables you to perform basic operations on a KVM server using a private API key. The library offers functionalities like:

- Get server configuration
- Get server status
- Start server
- Stop server
- Restart server

## Installation

To install FireAPI:

```bash
# Clone the repository
git clone https://github.com/EvickaStudio/24-Fire-REST-API.git
# Change directory
cd 24-Fire-REST-API
```

Ensure you have Python 3.x installed on your system.
I am currently trying to get the package on PyPi, but i am having some issues with it.

You can build the package yourself using the following command:

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

Once the instance is created, you can interact with the 24Fire REST API using the methods provided:

```python
# Get server config
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

For more information on the 24Fire REST API, consult the [original documentation](https://documenter.getpostman.com/view/18955936/2s93zB6hJu).
