from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='textscribe',
  version='0.0.1',
  description='Easily Structuring Data',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Hunter Thomas',
  author_email='waidai2027@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='data structure', 
  packages=find_packages(),
  install_requires=[''] 
)