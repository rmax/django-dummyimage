#!/usr/bin/env python

import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

setup(
    name = "dummyinage",
    description = "Dynamic Dummy Image Generator For Django!",
    author = "Rolando Espinoza La fuente",
    author_email = "darkrho@gmail.com",
    url = "https://github.com/darkrho/django-dummyimage",
    version = "0.05",
    packages = find_packages(),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
)
