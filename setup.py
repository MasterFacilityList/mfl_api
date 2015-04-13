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
    install_requires=[
        "model_mommy>=1.2",
        "Fabric>=1.10",
        "coverage>=3.7",
        "psycopg2>=2.5",
        "djangorestframework>=3.1",
        "django-filter>=0.9",
        "flake8>=2.3",
        "django-cors-headers>=1.0",
        "virtualenv>=12.0",
        "pip>=6.0",
        "tox>=1.9",
        "djangorestframework-xml>=1.0",
        "djangorestframework-csv>=1.3",
        "django>=1.8",
    ],
)
