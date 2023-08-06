# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
data collect package setup
"""
import setuptools

setuptools.setup(
    packages=setuptools.find_packages(),
    platforms="any",
    install_requires=[
        "pybind11>=2.0.1",
        "Pillow>=4.2.0",
        "numpy>=1.21.6",
        "pydantic>=1.10.4",
        "spdlog>=2.0.4",
        "opencv-python-headless"
    ],
    setup_requires=["pybind11"]
)