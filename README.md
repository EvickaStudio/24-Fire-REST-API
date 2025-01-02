# FireAPI

[![PyPI version](https://badge.fury.io/py/fireapi.svg)](https://badge.fury.io/py/fireapi)
[![Downloads](https://pepy.tech/badge/fireapi)](https://pepy.tech/project/fireapi)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fireapi.svg)](https://pypi.org/project/fireapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

## Overview

FireAPI is a Python client library that provides convenient access to the [24Fire REST API](https://apidocs.24fire.de/), allowing you to control KVM server functions using a private API key. The library supports both synchronous and asynchronous operations and includes type definitions for all request parameters and response fields.

Features:
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
  - [Development](#development)
    - [Setup](#setup)
    - [Running Tests](#running-tests)
    - [Code Style](#code-style)
    - [Making Releases](#making-releases)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

Install FireAPI using pip:

```bash
pip install fireapi
```

For development version:
```bash
pip install --pre fireapi
```

## Usage

The FireAPI library provides both synchronous and asynchronous clients.

### Synchronous Usage

```python
from fireapi import FireAPI

api_key = "your-api-key-here"
fire_api = FireAPI(api_key)

# Get server configuration
config = fire_api.vm.get_config()
print(f"Server Configuration: {config}")

# Get server status
status = fire_api.vm.get_status()
print(f"Server Status: {status}")

# Power management
fire_api.vm.start()    # Start the server
fire_api.vm.stop()     # Stop the server
fire_api.vm.restart()  # Restart the server

# Backup management (24fire+ only)
backups = fire_api.backup.list()
backup = fire_api.backup.create(description="My backup")
fire_api.backup.delete(backup_id=backup.data["backup_id"])

# Monitoring (24fire+ only)
timings = fire_api.monitoring.get_timings()
incidences = fire_api.monitoring.get_incidences()
```

### Asynchronous Usage

```python
import asyncio
from fireapi import AsyncFireAPI

async def main():
    api_key = "your-api-key-here"
    async with AsyncFireAPI(api_key) as fire_api:
        # Get server configuration
        config = await fire_api.vm.get_config()
        print(f"Server Configuration: {config}")

        # Get server status
        status = await fire_api.vm.get_status()
        print(f"Server Status: {status}")

        # Power management
        await fire_api.vm.start()    # Start the server
        await fire_api.vm.stop()     # Stop the server
        await fire_api.vm.restart()  # Restart the server

asyncio.run(main())
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/EvickaStudio/24-Fire-REST-API.git
cd 24-Fire-REST-API
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

### Running Tests

Run tests with tox:
```bash
tox
```

Or run specific environments:
```bash
tox -e lint     # Run linting
tox -e type     # Run type checking
tox -e py39     # Run tests on Python 3.9
```

### Code Style

The project uses:
- [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [MyPy](https://mypy.readthedocs.io/) for type checking
- [Pre-commit](https://pre-commit.com/) for git hooks

Format code:
```bash
tox -e format
```

### Making Releases

1. For stable releases:
```bash
.\release.bat
# Enter version number when prompted (e.g., 1.0.0)
```

2. For development releases:
```bash
.\dev-release.bat
```

## Documentation

The API documentation can be found [here](https://apidocs.24fire.de/).

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the [MIT License](LICENSE).
