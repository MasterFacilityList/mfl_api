from setuptools import setup, find_packages

with open('README.rst') as readme:
    description = readme.read()


setup(
    name='mfl',
    version='2.0.0',
    description='Master falicity list',
    long_description=(description),
    author='Savannah Developers',
    author_email='developers@savannahinformatics.com',
    url='',
    packages=find_packages(),
    install_requires=[],
)
