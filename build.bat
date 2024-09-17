@echo off
setlocal enabledelayedexpansion

:: Check if version.py file exists
if not exist src\fireapi\version.py (
    echo version.py file not found.
    exit /b 1
)

:: Prompt for version update type
set /p versionType="Enter version update type (major, minor, patch): "

:: Read the current version from version.py
for /f "tokens=3 delims= " %%i in ('findstr /r /c:"__version__ = " src\fireapi\version.py') do (
    set currentVersion=%%i
)

:: Remove quotes from the version string
set currentVersion=%currentVersion:~1,-1%

:: Split the version into major, minor, and patch
for /f "tokens=1,2,3 delims=." %%a in ("%currentVersion%") do (
    set major=%%a
    set minor=%%b
    set patch=%%c
)

:: Increment the version based on user input
if "%versionType%"=="major" (
    set /a major+=1
    set minor=0
    set patch=0
) else if "%versionType%"=="minor" (
    set /a minor+=1
    set patch=0
) else if "%versionType%"=="patch" (
    set /a patch+=1
) else (
    echo Invalid version type.
    exit /b 1
)

:: Form the new version string
set newVersion=%major%.%minor%.%patch%

:: Update version.py with the new version (no trailing space or newline)
(
    echo __version__ = "%newVersion%"
) > src\fireapi\version.py

:: Run black for code formatting
black .
if errorlevel 1 (
    echo Code formatting failed.
    exit /b 1
)

:: Build the library
python -m build

:: Upload to PyPI
twine upload dist/*

endlocal