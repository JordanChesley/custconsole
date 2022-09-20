from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name='custconsole',
    version='1.0.0',
    description='Create a customizable CLI for your application(s).',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Jordan Chesley',
    author_email='jordan.r.chesley@gmail.com',
    url='https://github.com/JordanChesley/custconsole',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
    ],
    packages=find_packages()
)
