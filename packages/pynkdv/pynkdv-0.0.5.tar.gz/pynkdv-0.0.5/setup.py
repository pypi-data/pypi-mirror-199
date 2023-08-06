#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='pynkdv',
    version='0.0.5',
    author='rui',
    author_email='19251017@life.hkbu.edu.hk',
    url='https://github.com/ZangRui-666/pynkdv',
    description='for nkdv in python',
    packages=['pynkdv'],
    install_requires=['nkdv', 'osmnx', 'pandas', 'shapely'],
    entry_points={
    }
)