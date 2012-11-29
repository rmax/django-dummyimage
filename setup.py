#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "django-dummyimage",
    version = "0.1.1",
    description = "Dynamic Dummy Image Generator For Django!",
    author = "Rolando Espinoza La fuente",
    author_email = "darkrho@gmail.com",
    url = "https://github.com/darkrho/django-dummyimage",
    license = "BSD",
    packages = find_packages(),
    zip_safe=False, # because we're including media that Django needs
    include_package_data = True,
    install_requires = [
        'django',
        'pil',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
)
