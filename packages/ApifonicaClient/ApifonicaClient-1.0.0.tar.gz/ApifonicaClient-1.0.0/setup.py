from setuptools import setup, find_packages

setup(
    name="ApifonicaClient",
    version="1.0.0",
    description="Unofficial Python Package to easily integrate the Apifonica API to your project",
    author="Paul Harrer",
    author_email="mail@paulharrer.at",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
)
