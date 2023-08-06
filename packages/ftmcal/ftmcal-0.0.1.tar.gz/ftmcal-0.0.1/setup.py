from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.11'
]

setup(
  name='ftmcal',
  version='0.0.1',
  description='A simple calculator library for practice.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Fateme .Fa',
  author_email='fatemefallah99@gmail.com',
  license='OSI Approved :: MIT License', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[''] 
)
