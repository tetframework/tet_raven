# -*- coding: utf-8 -*-
from __future__ import absolute_import, division,\
       print_function, unicode_literals

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = """
    tet
    raven
""".split()

setup(name='tet_raven',
      version='0.1',
      description='Unearthly intelligent batteries-included application framework built on Pyramid',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Development Status :: 1 - Planning",
          "Framework :: Pyramid",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Python Software Foundation License",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Topic :: Internet :: WWW/HTTP :: WSGI",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
          "Topic :: Software Development :: Libraries :: Application Frameworks"
      ],
      author='Antti Haapala',
      author_email='antti@haapala.name',
      url='http://anttipatterns.com',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='tet_raven',
      install_requires=requires,
)
