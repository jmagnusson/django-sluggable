#!/usr/bin/env python
from setuptools import setup

setup(
    name='django-sluggable',
    version='1.0.2',
    description='Automatically generated unique model slugs for Django models.',
    install_requires=['Django', 'six'],
    author='Ted Kaemming',
    author_email='ted@kaemming.com',
    url='http://www.github.com/tkaemming/django-sluggable/',
    packages=['sluggable'],
)
