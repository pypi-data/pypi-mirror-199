# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 21:18:48 2023

@author: ajayd
"""

from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='bhavcopy',
  version='2.0',
  description='Download NSE Bhavcopy Data',
  long_description=open('README.txt').read(),
  url='',  
  author='Ajay',
  author_email='ajaydpawar@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='Bhavcopy', 
  packages=find_packages(),
  install_requires= ['pandas', 'numpy', 'requests']
)