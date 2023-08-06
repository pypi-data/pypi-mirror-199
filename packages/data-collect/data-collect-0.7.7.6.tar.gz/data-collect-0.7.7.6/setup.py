# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
data collect package setup
"""
import setuptools
from pybind11 import __version__

print("pybind11 version: {}".format(__version__))
setuptools.setup(
    name="data-collect",
    version="0.7.7.6",
    author="Baidu",
    packages=setuptools.find_packages(),
    platforms="any",
    install_requires=[
        "spdlog>=2.0.4",
        "Pillow>=4.2.0",
        "numpy>=1.21.6",
        "pydantic>=1.10.4",
        "opencv-python-headless"
    ],
    setup_requires=["pybind11"]
)