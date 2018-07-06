import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arukas",
    version="0.0.5",
    author="eternal-flame-AD",
    author_email="ef@eternalflame.cn",
    description="Arukas.io api wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eternal-flame-AD/arukas-python-sdk",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0",
        "Operating System :: OS Independent",
    ),
)