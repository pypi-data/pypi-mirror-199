# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
data collect package setup
"""
import setuptools

setuptools.setup(
    name='data_collect',
    install_requires=[
        'pybind11',
        'opencv-python-headless',
        'Pillow>=9.2.0',
        'numpy>=1.21.6',
        'pydantic>=1.10.4',
        'spdlog>=2.0.4',
    ],
)