# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="datahub",
    version="0.0.1",
    author="Harshal Sheth",
    author_email='harshal@acryl.io',
    url="https://pypi.python.org/pypi/acryl-datahub",
    download_url="https://pypi.org/project/acryl-datahub/",
    description="Screen-scraping library",
    long_description="""Use `acryl-datahub <https://pypi.org/project/acryl-datahub/>`_ instead.""",    # noqa
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
