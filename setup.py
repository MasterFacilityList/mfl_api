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
    url='',
    packages=find_packages(),
    include_package_data=True,
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
    install_requires=[],
)
