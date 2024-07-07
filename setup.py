from distutils.core import setup

setup(
    name="fireapi",  # Package name
    packages=["fireapi"],  # Same as "name"
    version="0.2",  # Start version
    license="AGPL-3.0",  # License type updated to AGPL-3.0
    description="A simple API wrapper for the 24Fire REST API",  # Short description
    author="EvickaStudio",  # Your name
    author_email="hello@evicka.de",  # Your email
    url="https://github.com/EvickaStudio/24-Fire-REST-API",  # GitHub repository URL
    keywords=["API", "24Fire", "KVM", "Server Management"],  # Keywords
    install_requires=[
        "aiohttp",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
