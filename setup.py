#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='sshlauncher',
      version='0.2.0',
      description='Quickly ssh/mount/unmount into another machine',
      author='Joao Cordeiro',
      author_email='jlcordeiro@gmail.com',
      url='https://github.com/jlcordeiro/py-sshlauncher',
      platforms=['all'],
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7'
      ],
      py_modules=['sserver','systemcalls'],
      scripts=['sshlauncher.py'],
      )
