from setuptools import setup, find_packages

setup(
  name='custconsole',
  version='0.0.5',
  description='Create a customizable console(s) for your program.',
  author='Jordan Chesley',
  author_email='jordan.r.chesley@gmail.com',
  url='https://github.com/JordanChesley/custconsole',
  license='MIT',
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
  packages=find_packages(),
  install_requires=['cryptography']
)
