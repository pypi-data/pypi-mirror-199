#!/usr/bin/env python3
from setuptools import setup, find_packages
from toolboxdir.version import __version__

# NOTE: Update the __version__ flag in quikey/version.py for release.

setup(
    name="toolbox-dir",
    version=__version__,
    packages=find_packages(),
    author="bostrt",
    entry_points={
        "console_scripts": ["tb=toolboxdir.toolboxdir:cli"]
    },
    description="Shortcut tool for Toolbox (https://containertoolbx.org/) that can associated diretories with a toolbox.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="",
    url="https://github.com/bostrt/toolbox-dir",
    install_requires=[
        "click",
        "pyxdg",
        "podman",
    ],
)
