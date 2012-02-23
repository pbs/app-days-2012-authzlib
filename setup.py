#!/usr/bin/env python
import os
from setuptools import setup, find_packages


"""The path to the README file."""
README_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'README.rst')


"""Setup entry for the package."""
setup(
    name='authzlib',
    version='0.1',
    description='Client library for the PBS Authz service',
    long_description=open(README_PATH, 'r').read(),
    author='Ion Scerbatiuc',
    author_email='authz@pbs.org',
    url='http://authz.pbs.org/',
    packages=find_packages(),
    setup_requires=['s3sourceuploader']
)
