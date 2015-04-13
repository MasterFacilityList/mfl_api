#! /usr/bin/env python
from os.path import dirname, abspath

from fabric.api import local
from fabric.api import lcd


BASE_DIR = dirname(abspath(__file__))


def test():
    with lcd(BASE_DIR):
        local('pip install tox')
        local('tox')


def run():
    local('{}/manage.py runserver 8000'.format(BASE_DIR))


def deploy():
    """
    Should be run only by the release manager
    """
    local('python setup.py sdist upload -r slade')
