@echo off
setlocal enabledelayedexpansion

:: Clean previous builds
if exist "dist" rd /s /q "dist"
if exist "build" rd /s /q "build"
if exist "*.egg-info" rd /s /q "*.egg-info"

:: Format and check code
echo Running code checks...
ruff format .
if errorlevel 1 (
    echo Code formatting failed.
    exit /b 1
)

ruff check . --fix
if errorlevel 1 (
    echo Ruff checks failed.
    exit /b 1
)

mypy src/fireapi
if errorlevel 1 (
    echo Type checking failed.
    exit /b 1
)

:: Ensure all changes are committed
git diff --quiet
if errorlevel 1 (
    echo There are uncommitted changes. Please commit them first.
    exit /b 1
)

:: Build the development package
echo Building development package...
python -m build
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

:: Ask for confirmation before uploading
set /p upload="Do you want to upload the development version to PyPI? (y/n): "
if /i "%upload%"=="y" (
    echo Uploading to PyPI...
    twine upload --skip-existing dist/*
)

echo Development release process completed.
endlocal
