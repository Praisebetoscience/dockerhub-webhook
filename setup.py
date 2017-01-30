"""dockerhub_webhook setup.py"""
# -*- coding: utf-8 -*-
import os
import codecs
import re

from setuptools import setup, find_packages

PACKAGE_NAME = 'dockerhub-webhook'
HERE = os.path.dirname(__file__)
with codec.open(os.path.join(HERE, 'README.md'), encoding='utf8') as file:
    README = file.read()


def read(*subpaths):
    path = os.path.join(HERE, *subpaths)
    with codecs.open(path, encoding='utf8') as file:
        return file.read()


def get_metavar(metavar, *paths):
    file = read(*paths)
    version_pattern = r'''^__{}__\s*=\s*['"](?P<var>.*)['"]'''.format(metavar)
    var_match = re.search(version_pattern, file, re.M)

    if var_match:
        return var_match.group('var')
    raise RuntimeError('{} string not found'.format(metavar))


install_requires = [
    'requests ==2.13.0',
    'Flask ==0.12'
]

tests_require = [
    'pytest >=3.0.6',
    'pytest-mock >=1.5.0'
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
      keywords='dockerhub webhook handler'
      license=get_metavar('license', 'dockerhook', '__init__.py'),
      packages=find_packages(exclude=['tests.*', 'tests', 'venv']),
      package_data={'', 'LICENSE'},
      install_requires=install_requires,
      setup_requires=setup_requires,
      tests_require=tests_require,
      test_suite='tests',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
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
