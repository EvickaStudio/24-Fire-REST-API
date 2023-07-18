# FireAPI

FireAPI is a Python wrapper for the 24Fire REST API that allows you to control basic functions of a KVM server with a private API key. The wrapper provides the following features:

- Get server configuration
- Get server status
- Start server
- Stop server
- Restart server

## Installation

To use FireAPI, you need to have Python 3 installed on your system. You can import it with: `import fireapi`


## Usage

To use FireAPI, you need to create an instance of the `FireAPI` class with your API key:

```python
from fireapi import FireAPI

API_KEY = "your-api-key-here"
fire_api = FireAPI(API_KEY)
```
You can then use the methods of the `FireAPI` class to interact with the 24Fire REST API:
```python
# Get server config
config = fire_api.get_config()
print(config)

# Get server status
status = fire_api.get_status()
print(config)

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

## Info
Read the original documentation on [https://documenter.getpostman.com/view/18955936/2s93zB6hJu](https://documenter.getpostman.com/view/18955936/2s93zB6hJu)
