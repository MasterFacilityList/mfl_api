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
