#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='hopak',
      version='0.5.1',
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
      include_package_data=True,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],


      package_data = {
        'hopak': [
            'templates/*.html',
            'templates/widgets/*.html',
        ]
    }
)
