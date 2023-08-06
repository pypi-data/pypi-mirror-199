#!/usr/bin/env python
from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name='opencdms_test_databases',
    version="0.1.9",
    description='OpenCDMS test databases',
    license="MIT license",
    long_description=readme + "\n",
    long_description_content_type='text/markdown',
    author='OpenCDMS',
    author_email='info@opencdms.org',
    maintainer='Ian Edwards',
    maintainer_email='info@opencdms.org',
    url='https://github.com/opencdms/opencdms-test-databases',
    keywords="opencdms",
    packages=['opencdms_test_databases'],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
