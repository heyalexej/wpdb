#!/usr/bin/python3

import sys

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

if sys.version_info[0] != 3:
  print("Error: python 3 is required.")
  exit()

with open('LICENSE') as f:
  install_license = f.read()

setup(
  # Application name:
  name='wpdb',

  # Version number:
  version='0.1',

  # Application author details:
  author="Dongjin Lee",
  author_email="dongjin.lee.kr@gmail.com",

  # Packages
  py_modules = ['wpdb'],

  # Details
  url="https://github.com/dongjinleekr/wpdb",

  #
  license=install_license,
  description="SQLAlchemy ORM mapping to wordpress database.",

  long_description=
"""\
SQLAlchemy ORM mapping to wordpress database.
""",

  # Dependent packages (distributions)
  install_requires=[
    'SQLAlchemy==0.9.8',
  ]
)

