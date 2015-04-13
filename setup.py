from __future__ import print_function

import io

from setuptools import setup, find_packages

with open('README.rst') as readme:
    description = readme.read()


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')


setup(
    name='mfl',
    version='2.0.0',
    license='MIT License',
    description='Master falicity list',
    long_description=(description),
    author='Savannah Informatics Limitee Developers',
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
    install_requires=[],
)
