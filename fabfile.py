#! /usr/bin/env python
from os.path import dirname, abspath

from fabric.api import local


BASE_DIR = dirname(abspath(__file__))


def test():
    local('python setup.py check')
    local('pip install tox')
    local('tox -r -c tox.ini')


def run():
    local('{}/manage.py runserver 8000'.format(BASE_DIR))


def deploy():
    """
    Should be run only by the release manager
    """
    local('python setup.py sdist upload -r slade')
