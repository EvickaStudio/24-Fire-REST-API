from distutils.core import setup

# Read the contents of your README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fireapi",
    packages=["fireapi"],
    version="0.4",
    license="AGPL-3.0",
    description="A simple API wrapper for the 24Fire REST API",
    long_description=long_description,  # Set the long description
    long_description_content_type="text/markdown",  # Specify the content type. Important for rendering markdown!
    author="EvickaStudio",
    author_email="hello@evicka.de",
    url="https://github.com/EvickaStudio/24-Fire-REST-API",
    keywords=["API", "24Fire", "KVM", "Server Management"],
    install_requires=[
        "aiohttp", "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
