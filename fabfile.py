# -*- coding: utf-8 -*-

# http://docs.fabfile.org/en/1.5/tutorial.html

from fabric.api import *

project = "fbone"

# the user to use for the remote commands
env.user = ''
# the servers where the commands are executed
env.hosts = ['']


def reset():
    """
    Reset local debug env.
    """

    local("rm -rf /tmp/fbone.sqlite instance/logs instance/uploads instance/openid")
    local("mkdir instance/logs instance/uploads instance/openid")
    local("python manage.py initdb")


def babel():
    """
    Babel compile.
    """

    local("python setup.py compile_catalog --directory `find -name translations` --locale zh -f")


def run():
    local("python manage.py run")


def r():
    run()


def d():
    """
    Debug.
    """

    reset()
    run()
