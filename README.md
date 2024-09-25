# FireAPI

[![PyPI version](https://badge.fury.io/py/fireapi.svg)](https://badge.fury.io/py/fireapi)
[![Downloads](https://pepy.tech/badge/fireapi)](https://pepy.tech/project/fireapi)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fireapi.svg)](https://pypi.org/project/fireapi/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Overview

FireAPI is a Python library that serves as a wrapper for the 24Fire REST API. It allows you to perform basic operations on a KVM server using a private API key. The library provides the following functionalities:

* Get server configuration
* Get server status
* Start server
* Stop server
* Restart server
* Delete backup (exclusive to `24fire+` subscribers)
* Create backup (exclusive to `24fire+` subscribers)
* List all backups (exclusive to `24fire+` subscribers)
* Retrieve monitoring timings (exclusive to `24fire+` subscribers)
* Retrieve monitoring incidences (exclusive to `24fire+` subscribers)
* Async Support

> [!NOTE]
> Disclaimer: Unable to test `24fire+` exclusive features due to lack of subscription. If you encounter issues, please report them on GitHub.

## Table of Contents

- [FireAPI](#fireapi)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Synchronous Usage](#synchronous-usage)
    - [Asynchronous Usage](#asynchronous-usage)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

To install FireAPI, use pip:

```bash
pip install fireapi
```

Alternatively, you can build and install the package manually:

```bash
git clone https://github.com/EvickaStudio/24-Fire-REST-API.git
cd 24-Fire-REST-API
python -m build
pip install ./
```

## Usage

### Synchronous Usage

To get started, import the `FireAPI` class from the `fireapi` package and instantiate it using your API key:

```python
from fireapi import FireAPI

apiKey = "your-api-key-here"
fireApi = FireAPI(apiKey)
```

Once the instance is created, you can interact with the 24Fire REST API using the provided methods:

```python
# Get server configuration
config = fireApi.vm.getConfig()
print(config)

# Get server status
status = fireApi.vm.getStatus()
print(status)

# Start server
start = fireApi.vm.startServer()
print(start)

# Stop server
stop = fireApi.vm.stopServer()
print(stop)

# Restart server
restart = fireApi.vm.restartServer()
print(restart)

# Delete a backup
delete_backup = fireApi.backup.deleteBackup("backup_id")

# Create a backup
create_backup = fireApi.backup.createBackup("Backup description")

# List all backups
backups = fireApi.backup.listBackup()

# Retrieve monitoring timings
timings = fireApi.monitoring.timings()

# Retrieve monitoring incidences
incidences = fireApi.monitoring.incidences()
```

### Asynchronous Usage

When using the `async` methods, you can use the `await` keyword to wait for the response:

```python
import asyncio
from fireapi import AsyncFireAPI

async def main():
    apiKey = "your-api-key-here"
    try:
        fireApi = AsyncFireAPI(apiKey)
        # Get server configuration
        config = await fireApi.vm.getConfig()
        print(config)
        # And the other methods that FireAPI provides
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

For more information on the 24Fire REST API, refer to the [original documentation](https://apidocs.24fire.de/).

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/EvickaStudio/24-Fire-REST-API).

## License

This project is licensed under the [AGPL v3 License](LICENSE).
