# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
data collect package setup
"""
import setuptools

setuptools.setup(
    setup_requires=['pybind11>=2.4.2'],
    packages=setuptools.find_packages(),
)