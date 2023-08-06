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
    setup_requires=['pybind11>=2.2'],
    install_requires=[
        'pybind11>=2.2',
        'spdlog>=2.0.4',
        'opencv-python-headless',
        'Pillow',
        'numpy',
        'pydantic',
    ],
)