#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup


def read_file(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as r:
        return r.read()


README = read_file("README.rst")
CONTRIB = read_file("CONTRIBUTING.rst")
CHANGES = read_file("CHANGES.rst")
version = read_file("VERSION.txt").strip()


setup(
    name="RepkaPi.GPIO",
    version=version,
    author="@screatorpro",
    description=("A drop-in replacement for RPi.GPIO for the Repka Pi"),
    long_description="\n\n".join([README, CONTRIB, CHANGES]),
    license="MIT",
    keywords="Repka Pi RepkaPi gpio",
    url="https://github.com/DikShv/RepkaPi.GPIO",
    packages=["RepkaPi"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
