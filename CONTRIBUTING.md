# Contributing to FireAPI

Thank you for your interest in contributing to FireAPI! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a welcoming, inclusive, and harassment-free environment. Please be respectful and constructive in your communications with others.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/EvickaStudio/24-Fire-REST-API.git
   cd 24-Fire-REST-API
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .[dev]
   ```
4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Process

### Setting Up Your Development Environment

1. Make sure you have Python 3.7 or higher installed
2. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```
3. Configure your IDE to use:
   - Ruff for linting and formatting
   - MyPy for type checking
   - Pre-commit hooks for git

### Making Changes

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run tests and checks:
   ```bash
   tox
   ```
4. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

### Code Style

We use several tools to maintain code quality:

- **Ruff** for linting and formatting
- **MyPy** for type checking
- **Pre-commit** hooks for automated checks

To format your code:
```bash
tox -e format
```

To run linting:
```bash
tox -e lint
```

To run type checking:
```bash
tox -e type
```

### Testing

1. Write tests for new features
2. Run the test suite:
   ```bash
   tox
   ```
3. Ensure all tests pass before submitting your changes

## Pull Request Process

1. Update the documentation to reflect any changes
2. Run the full test suite using `tox`
3. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Create a Pull Request on GitHub
5. Describe your changes in detail:
   - What problem does it solve?
   - What changes have you made?
   - Any breaking changes?
6. Reference any related issues

### Pull Request Guidelines

- Keep changes focused and atomic
- Follow the existing code style
- Include tests for new features
- Update documentation as needed
- Ensure CI checks pass

## Documentation

If you're adding new features or making changes, please update the documentation:

1. Update docstrings in the code
2. Update relevant files in the `docs/` directory
3. Add examples if appropriate
4. Update the README.md if needed

## Release Process

Releases are managed by the maintainers. If you need a new release:

1. Open an issue requesting a release
2. Include what changes need to be released
3. Maintainers will:
   - Review the changes
   - Update version numbers
   - Create a new release
   - Publish to PyPI

## Getting Help

If you need help:

1. Check the [documentation](docs/)
2. Open an issue with questions
3. Ask in pull request comments

## License

By contributing to FireAPI, you agree that your contributions will be licensed under the MIT License.
