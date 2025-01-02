# FireAPI

[![PyPI version](https://badge.fury.io/py/fireapi.svg)](https://badge.fury.io/py/fireapi)
[![Downloads](https://pepy.tech/badge/fireapi)](https://pepy.tech/project/fireapi)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fireapi.svg)](https://pypi.org/project/fireapi/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Overview

FireAPI is a Python client library that provides convenient access to the [24Fire REST API](https://apidocs.24fire.de/), allowing you to control KVM server functions using a private API key. The library supports both synchronous and asynchronous operations and includes type definitions for all request parameters and response fields.

- Get server configuration
- Get server status
- Start, stop, and restart the server
- Backup management (create, delete, list) *(exclusive to `24fire+` subscribers)*
- Retrieve monitoring timings and incidences *(exclusive to `24fire+` subscribers)*

> [!NOTE]
> Some features are exclusive to `24fire+` subscribers and have not been tested due to lack of subscription. If you encounter issues, please report them on GitHub.

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
  - [Alert](#alert)
    - [Non-Permissive License](#non-permissive-license)

## Installation

Install FireAPI using pip:

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

The FireAPI library provides both synchronous and asynchronous clients.

### Synchronous Usage

Import the `FireAPI` class and instantiate it with your API key:

```python
from fireapi import FireAPI

api_key = "your-api-key-here"
fire_api = FireAPI(api_key)
```

Use the provided methods to interact with the API:

```python
# Get server configuration
config = fire_api.vm.get_config()
print(config)

# Start the server
response = fire_api.vm.start_server()
print(response)
```

For more examples, see the [synchronous example](examples/synchronous_example.py).

### Asynchronous Usage

Import the `AsyncFireAPI` class and use it within an asynchronous function:

```python
import asyncio
from fireapi import AsyncFireAPI

async def main():
    api_key = "your-api-key-here"
    fire_api = AsyncFireAPI(api_key)
    
    # Get server configuration
    config = await fire_api.vm.get_config()
    print(config)
    
    # Start the server
    response = await fire_api.vm.start_server()
    print(response)

asyncio.run(main())
```

For more examples, see the [asynchronous example](examples/asynchronous_example.py).

## Documentation

The API documentation can be found [here](https://apidocs.24fire.de/).

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/EvickaStudio/24-Fire-REST-API).

## License

This project is licensed under the [MIT License](LICENSE).

## Alert

### Non-Permissive License

I noticed that this project uses a license which requires less permissive conditions such as disclosing the source code, stating changes, or redistributing the source under the same license. It is advised to further consult the license terms before use.
