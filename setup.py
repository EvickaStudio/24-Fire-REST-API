from distutils.core import setup

setup(
    name="fireapi",  # Package name
    packages=["fireapi"],  # Same as "name"
    version="0.1",  # Start version
    license="MIT",  # License type
    description="A simple API wrapper for the 24Fire REST API",  # Short description
    author="EvickaStudio",  # Your name
    author_email="kirenogfx@gmail.com",  # Your email
    url="https://github.com/EvickaStudio/24-Fire-REST-API",  # GitHub repository URL
    keywords=["API", "24Fire", "KVM", "Server Management"],  # Keywords
    install_requires=[
        "requests",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
