from setuptools import setup, find_packages

setup(
    name='fireapi',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='EvickaStudio',
    description='A simple API wrapper for the 24Fire REST API',
)
