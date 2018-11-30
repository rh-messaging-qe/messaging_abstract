# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

from setuptools import setup, find_packages

files = ["*"]

setup(
    name='messaging_abstract',
    version='0.1.1',
    packages=find_packages(),
    package_data={'messaging_abstract': files},
    license='Apache 2.0',
    description='',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock', 'pytest-mock'],
    install_requires=[
        '',
    ],
    url='https://github.com/rh-messaging-qe/messaging_abstract',
    author='Dominik Lenoch',
    author_email='dlenoch@redhat.com'
)
