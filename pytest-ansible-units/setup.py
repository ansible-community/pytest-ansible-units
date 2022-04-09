#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-ansible-units',
    version='0.0.1',
    author='Bradley A. Thornton',
    author_email='bthornto@redhat.com',
    maintainer='Bradley A. Thornton',
    maintainer_email='bthornto@redhat.com',
    license='GNU GPL v3.0',
    url='https://github.com/cidrblock/pytest-ansible-units',
    description='A pytest plugin for running unit tests within an ansible collection',
    long_description=read('README.rst'),
    py_modules=['pytest_ansible_units'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        'pytest11': [
            'ansible-units = pytest_ansible_units',
        ],
    },
)
