# backend/setup.py
from setuptools import setup, find_packages

setup(
    name="issue_tracker",
    version="0.1.0",
    packages=find_packages(where="app") + ["app"],
    package_dir={"": "app"},
)
