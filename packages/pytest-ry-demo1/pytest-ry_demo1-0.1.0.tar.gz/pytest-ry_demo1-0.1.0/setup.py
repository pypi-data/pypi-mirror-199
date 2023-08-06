#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-ry_demo1',
    version='0.1.0',
    author='ryhn',
    author_email='xuehy@tomtaw.com.cn',
    maintainer='ryhn',
    maintainer_email='xuehy@tomtaw.com.cn',
    license='BSD-3',
    url='https://github.com/ryhn0412/pytest-ry_demo',
    description='测试',
    long_description='测试是搜索是是',
    py_modules=['pytest_ry_demo'],
    python_requires='>=3.8',
    install_requires=['pytest>=3.5.0'],
    entry_points={
        'pytest11': [
            'ry_demo = pytest_ry_demo',
        ],
    },
)
