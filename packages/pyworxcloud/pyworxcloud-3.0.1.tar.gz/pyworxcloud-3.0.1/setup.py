# -*- coding: utf-8 -*-

import sys

import setuptools

if sys.version_info < (3, 10, 0):
    sys.exit("The pyWorxcloud module requires Python 3.10.0 or later")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyworxcloud",
    description="Landroid cloud API library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Malene Trab",
    author_email="malene@trab.dk",
    license="MIT",
    url="https://github.com/mtrab/pyworxcloud",
    packages=setuptools.find_packages(),
    project_urls={
        "Bug Tracker": "https://github.com/mtrab/pyworxcloud/issues",
    },
    install_requires=[
        "awsiot>=0.1.3",
        "urllib3>=1.26.10",
        "requests>=2.26.0",
    ],
)
