#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='hopak',
      version='0.5',
      description='hopak framework base package',
      long_description = open("README.rst").read(),
      author='Mikhail Kashkin',
      author_email='mkashkin@gmail.com',
      url='https://github.com/xen/hopak',
      # more examples here http://docs.python.org/distutils/examples.html#pure-python-distribution-by-package
      packages=['hopak', 'hopak.ds'],
      license = "BSD",
      install_requires=[
          'jinja2',
          'pyyaml'
      ],
      package_data = {
        'hopak': [
            'templates/*.html',
            'templates/widgets/*.html',
        ]
    }
     )
