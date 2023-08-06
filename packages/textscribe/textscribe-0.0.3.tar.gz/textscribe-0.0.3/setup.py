from setuptools import setup, Extension
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='textscribe',
  version='0.0.3',
  description='Easily Structuring Data',
  long_description='This library provides functionality for writing data to CSV and TXT files.',
  url='',  
  author='Hunter Thomas',
  author_email='waidai2027@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Structure data', 
  # packages=find_packages(),
  install_requires=[''] 
)
