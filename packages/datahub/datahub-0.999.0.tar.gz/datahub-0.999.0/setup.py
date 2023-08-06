# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="datahub",
    version="0.999.0",
    author="Acryl Data",
    author_email='harshal@acryl.io',
    url="https://pypi.python.org/pypi/acryl-datahub",
    download_url="https://pypi.org/project/acryl-datahub/",
    description="Dummy package for acryl-datahub",
    long_description="""This is a dummy package managed by the developers of acryl-datahub to prevent name squatting and ensure that folks who run `pip install datahub` end up with the right package. We recommend using`acryl-datahub <https://pypi.org/project/acryl-datahub/>`_ instead.""",
    license="MIT",
    install_requires=['acryl-datahub'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
