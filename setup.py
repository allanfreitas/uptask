# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('uptask/uptask.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_description = f.read().decode("utf-8")


setup(
    name = "uptask",
    packages = ["uptask"],
    entry_points = {
        "console_scripts": ['uptask = uptask.uptask:main']
        },
    version = version,
    description = "Task Runner(Local and SSH) made in Python.",
    long_description = long_description,
    author = "Allan Freitas",
    author_email = "allanfreitasci@gmail.com",
    url = "https://github.com/allanfreitas/uptask",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='tasks development runner',
    install_requires=[
        'python-dotenv==0.8.2',
        'paramiko==2.4.1',
        'colorama==0.3.4',
    ]
    )
