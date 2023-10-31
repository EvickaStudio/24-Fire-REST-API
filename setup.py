from distutils.core import setup

setup(
    name="fireapi",  # Package name
    packages=["fireapi"],  # Same as "name"
    version="0.1",  # Start version
    license="MIT",  # License type
    description="A simple API wrapper for the 24Fire REST API",  # Short description
    author="EvickaStudio",  # Your name
    author_email="evkrelay24@proton.me",  # Your email
    url="https://github.com/EvickaStudio/24-Fire-REST-API",  # GitHub repository URL
    download_url="https://github.com/EvickaStudio/24-Fire-REST-API/archive/refs/tags/v1.0.0.tar.gz",  # Download URL
    keywords=["API", "24Fire", "KVM", "Server Management"],  # Keywords
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Development status
        "Intended Audience :: Developers",  # Target audience
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",  # Supported Python versions
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
