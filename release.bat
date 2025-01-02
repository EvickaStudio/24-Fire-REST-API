@echo off
setlocal enabledelayedexpansion

:: Get the version from the user
set /p version="Enter the version number (e.g., 0.5.0): "

:: Validate version format
echo %version% | findstr /r "^[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo Invalid version format. Please use semantic versioning (e.g., 0.5.0)
    exit /b 1
)

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

:: Create and push git tag
echo Creating git tag v%version%...
git tag -a v%version% -m "Release version %version%"
if errorlevel 1 (
    echo Failed to create git tag.
    exit /b 1
)

git push origin v%version%
if errorlevel 1 (
    echo Failed to push git tag.
    exit /b 1
)

:: Build the package
echo Building package...
python -m build
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

:: Ask for confirmation before uploading
set /p upload="Do you want to upload to PyPI? (y/n): "
if /i "%upload%"=="y" (
    echo Uploading to PyPI...
    twine upload dist/*
)

echo Release process completed.
endlocal
