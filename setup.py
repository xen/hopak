#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='formgear',
      version='0.3.2',
      description='Form, mongodbengine objects',
      long_description = open("README.rst").read(),
      author='Mikhail Kashkin',
      author_email='mkashkin@gmail.com',
      url='https://github.com/xen/formgear',
      # more examples here http://docs.python.org/distutils/examples.html#pure-python-distribution-by-package
      packages=['formgear', ],
      license = "BSD",
      install_requires=[
          'jinja2',
          'pyyaml'
      ],
      package_data = {
        'formgear': [
            'templates/*.html',
            'templates/widgets/*.html',
        ]
    }
     )
