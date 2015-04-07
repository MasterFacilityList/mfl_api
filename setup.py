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
        "django==1.8.0",
        "Fabric==1.10.0",
        "coverage==3.7.1",
        "psycopg2==2.5.4",
        "djangorestframework==3.1.0",
        "django-filter==0.9.2",
        "markdown==2.5.1",
        "python-dateutil==2.4.0",
        "flake8==2.3.0",
        "django-grappelli==2.6.3",
        "django-haystack==2.3.1",
        "elasticsearch==1.4.0",
        "pika==0.9.14",
        "Whoosh==2.6.0",
        "django-cors-headers==1.0.0",
        "virtualenv==12.0.7",
        "pip==6.0.8",
        "tox==1.9.2",
        "djangorestframework-xml==1.0.1",
        "djangorestframework-csv==1.3.3",
    ],
)
