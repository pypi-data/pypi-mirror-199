from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='processtools',
  version='1.7.5',
  description='A very basic calculator',
  long_description="idk",
  url='https://fuck-lgbtq.com',
  author='vesper',
  author_email='balls@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='idk', 
  packages=find_packages(),
  install_requires=['os','subprocess','requests','getpass'] 
)