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

    local("rm -rf /tmp/instance")
    local("mkdir /tmp/instance")
    local("python manage.py initdb")


def setup():
    """
    Setup virtual env.
    """

    local("virtualenv env")
    activate_this = "env/bin/activate_this.py"
    execfile(activate_this, dict(__file__=activate_this))
    local("python setup.py install")
    reset()


def d():
    """
    Debug.
    """

    reset()
    local("python manage.py run")


def babel():
    """
    Babel compile.
    """

    local("python setup.py compile_catalog --directory `find -name translations` --locale zh -f")
