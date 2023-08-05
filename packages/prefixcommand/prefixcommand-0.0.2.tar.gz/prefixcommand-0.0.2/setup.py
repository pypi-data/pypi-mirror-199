#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="prefixcommand",
    url="https://gitlab.com/jjlee1/prefix",
    description="Run commands in 'environments', with a focus on prefix commands",
    package_dir={"": "src"},
    packages=find_packages("src"),
    platforms=["any"],
    zip_safe=True,
    version="0.0.2",
)
