# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from setuptools import setup


# Utility function to read the README- and VERSION-files.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="mox_solr",
    version=read("VERSION").strip(),
    author="Jørgen Gårdsted Jørgensen",
    author_email="jgj@magenta-aps.dk",
    description=("mox agent for synchronizing solr from os2mo"),
    license="MPL",
    keywords="sts solr os2mo lora",
    url="",
    packages=['mox_solr'],
    long_description=read('README.md').strip(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MPL License",
    ],
    install_requires=[
        # see requirements.txt
        # https://caremad.io/posts/2013/07/setup-vs-requirement/
    ]
)
