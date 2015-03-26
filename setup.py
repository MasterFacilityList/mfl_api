from setuptools import setup, find_packages

setup(
    name='mfl',
    version='2.0.0',
    description='Master falicity list',
    long_description=(''),
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    install_requires=[
        'Django==1.7.5',
        'psycopg2',
        'django-filter',
        'djangorestframework',
        'djangorestframework-camel-case',
    ],
)
