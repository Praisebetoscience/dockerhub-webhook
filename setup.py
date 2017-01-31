#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103

# setup.py
from codecs import open as copen
import os
import re
import sys

from setuptools import setup, find_packages


PACKAGE_NAME = 'dockerhub-webhook'
HERE = os.path.dirname(__file__)
with copen(os.path.join(HERE, 'README.md'), encoding='utf8') as fpt:
    README = fpt.read()

VERSION = get_metavar('version', 'dockerhook', '__init__.py')


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()


if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()


def read(*subpaths):
    path = os.path.join(HERE, *subpaths)
    with copen(path, encoding='utf8') as fobj:
        return fobj.read()


def get_metavar(metavar, *paths):
    metavar_file = read(*paths)
    metavar_patern = r'''^__{}__\s*=\s*['"](?P<var>.*)['"]'''.format(metavar)
    var_match = re.search(metavar_patern, metavar_file, re.M)

    if var_match:
        return var_match.group('var')
    raise RuntimeError('{} string not found'.format(metavar))


with copen(os.path.join(HERE, 'requirements.txt'), encoding='utf8') as fpt:
    install_requires = [l.strip() for l in fpt.readlines()]


tests_require = [
    'pytest >=3.0.6',
    'pytest-mock >=1.5.0',
    'pytest-cov >=2.4.0',
]

setup_requires = [
    'pytest-runner >=2.10.1'
]

setup(name=PACKAGE_NAME,
      version=get_metavar('version', 'dockerhook', '__init__.py'),
      description='Webhook handler for dockerhub autodeployments',
      long_description=README,
      author=get_metavar('author', 'dockerhook', '__init__.py'),
      author_email=get_metavar('email', 'dockerhook', '__init__.py'),
      url='https://github.com/Praisebetoscience/dockerhub-webhook',
      keywords='dockerhub webhook handler',
      license=get_metavar('license', 'dockerhook', '__init__.py'),
      packages=find_packages(exclude=['tests.*', 'tests', 'venv']),
      package_data={'': 'LICENSE'},
      install_requires=install_requires,
      setup_requires=setup_requires,
      tests_require=tests_require,
      test_suite='tests',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environmnt :: Console',
          'Framework :: Flask'
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Utilities'
      ]
      )
