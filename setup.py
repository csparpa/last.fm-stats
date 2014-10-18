#!/usr/bin/env python

from setuptools import setup

setup(
    name='lastfm_stats',
    version='0.2.0',
    description='Exercise on Last.fm data aggregation',
    author='Claudio Sparpaglione (@csparpa)',
    author_email='csparpa@gmail.com',
    url='http://github.com/csparpa/last.fm-stats',
    packages=['lastfm_stats', 'test'],
    license='MIT',
    test_suite='test'
)
