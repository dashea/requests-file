#!/usr/bin/env python

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requires = [line.strip() for line in open("requirements.txt").readlines()]

setup(
    name='requests-file',
    version='1.4.1',
    description='File transport adapter for Requests',
    author='David Shea',
    author_email='dshea@redhat.com',
    url='http://github.com/dashea/requests-file',
    py_modules=['requests_file'],
    install_requires=requires,
    license='Apache 2.0',
    test_suite='tests',
    classifiers=('Development Status :: 3 - Alpha',
                 'Environment :: Plugins',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.4'
                 )
    )
