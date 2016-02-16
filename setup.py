from __future__ import print_function

import io
import os
import sys
import config

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

with open('README.rst') as readme:
    description = readme.read()

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')
version = config.__version__


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setup(
    name='mfl',
    version=version,
    license='MIT License',
    author='Savannah Informatics Limited Developers',
    author_email='developers@savannahinformatics.com',
    description='Core APIs for the Kenyan Ministry of Health '
                'Master Facility List',
    long_description=long_description,
    url='https://github.com/MasterFacilityList/mfl_api',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Framework :: Django :: 1.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    install_requires=[
        "model_mommy>=1.2.4,<1.3.0",
        "Fabric>=1.10,<1.11.0",
        "coverage>=3.7,<3.8.0",
        "psycopg2>=2.5,<2.6.0",
        "djangorestframework>=3.1.0,<3.2.0",
        "django-filter>=0.9,<1.0.0",
        'dj_database_url>=0.3.0,<=0.4.0',
        "flake8==2.3",
        "django-cors-headers>=1.0,<1.1.0",
        "virtualenv>=12.0,<12.1.0",
        "pip>=6.0,<7.0.0",
        "tox>=1.9,<1.10.0",
        "djangorestframework-xml>=1.0,<1.1.0",
        "djangorestframework-csv>=1.3,<1.4.0",
        "django-rest-swagger>=0.2,<0.3.0",
        "Markdown>=2.5.1,<2.6.0",
        "django>=1.8,<1.9.0",
        'sqlparse>=0.1,<0.2.0',
        "pytest>=2.7,<2.8.0",
        "pytest-django>=2.8,<2.9.0",
        "pytest-xdist>=1.11,<1.12.0",
        "six>=1.9,<1.10.0",
        "django-reversion==1.9.3",
        "shapely>=1.5.7,<1.6.0",
        "wheel>=0.24.0,<1.25.0",
        "pytz>=2015.2",
        "werkzeug>=0.10.4,<0.11.0",
        "gunicorn>=19.3.0,<19.4.0",
        "ansible>=1.9.0,<1.10.0",
        "apache-libcloud>=0.17.0,<0.18..0",
        "django-environ>=0.3.0,<0.4.0",
        "python-coveralls>=2.5.0,<2.6.0",
        "djangorestframework-gis>=0.8.1,<0.9.0",
        "django-debug-toolbar>=1.3.0,<1.4.0",
        "django-rest-auth>=0.4.0,<0.5.0",
        "django-allauth>=0.19.1,<0.20.0",
        "django-oauth-toolkit>=0.8.1,<0.9.0",
        "drf-extensions>=0.2.7,<0.3.0",
        "xlsxwriter>=0.7.2,<0.8.0",
        "mock>=1.0.1,<1.1.0",
        "recommonmark>=0.1.1,<0.2.0",
        "WeasyPrint>=0.23,<0.24.0",
        "django-redis>=4.0.0,<4.1.0",
        "django-storages==1.1.8",
        "boto==2.38.0",
        "celery==3.1.19",
        "filechunkio==1.6"
    ],
)
