# -*- coding: utf-8 -*-
"""
Fabfile for managing a Python/Flask/Apache/MySQL project in MacOS/Ubuntu.
"""

import os

from fabric.api import env, task, run, local, get, sudo
from fabric.context_managers import cd, lcd, prefix, shell_env

PROJECT_NAME = "fbone"

# Remote Database Config
REMOTE_DB_USERNAME = ""
REMOTE_DB_PASSWORD = ""
REMOTE_DB_NAME = ""

# Local Database Config
LOCAL_DB_USERNAME = ""
LOCAL_DB_PASSWORD = ""
LOCAL_DB_NAME = ""

# the user to use for the remote commands
env.user = ''
# the servers where the commands are executed
env.hosts = ['']
# http://stackoverflow.com/questions/17102968/reading-logs-with-fabric
env.remote_interrupt = True


@task
def setup_python_macos():
    """Setup Python in MacOS via Homebrew"""

    # Setup Homebrew
    # TODO: Test if Homebrew installed?
    HOMEBREW_URL = "https://raw.githubusercontent.com/Homebrew/install/master/install"
    local("/usr/bin/ruby -e \"$(curl -fsSL %s)\"" % HOMEBREW_URL)
    local("echo export PATH=/usr/local/bin:/usr/local/sbin:$PATH >> ~/.bash_profile")

    # Setup Python
    local("brew install python")
    local("brew update")

    # Setup Virtualenv
    local("pip install virtualenvwrapper")
    local("echo source /usr/local/bin/virtualenvwrapper.sh >> ~/.bash_profile")


@task
def setup_python_ubuntu():
    """Setup Python in Ubuntu, which already comes with Python"""

    # Setup Virtualenv
    local("pip install virtualenvwrapper")
    local("echo source /usr/local/bin/virtualenvwrapper.sh >> ~/.bash_profile")


@task
def bootstrap():
    """Bootstrap in local"""

    local("rm -rf /tmp/instance")
    local("mkdir -p /tmp/instance/logs")
    local("mkdir -p /tmp/instance/uploads")

    with shell_env(FLASK_APP='wsgi.py', FLASK_DEBUG="1"):
        local("flask initdb")


@task
def bootstrap_production():
    """Bootstrap in production server"""
    pass


@task
def debug():
    """Run in debug mode in local"""

    with shell_env(FLASK_APP='wsgi.py', FLASK_DEBUG="1"):
        local("flask run")


@task(alias='t')
def test():
    """Run unittest in local"""

    with shell_env(FLASK_APP='wsgi.py', FLASK_DEBUG="1"):
        local("python tests.py")


@task
def deploy():
    """Deploy via Git"""

    local("cd " + os.path.join(os.environ["HOME"], PROJECT_NAME))
    local("git push")

    with cd(os.path.join("/home/wilson", PROJECT_NAME)):
        # Make sure git can be accessed via ssh
        run("git pull")
        # Make sure "WSGIScriptReloading On" in apache conf file
        run("touch wsgi.py")


@task
def syncdb():
    """Sync loacl db with remote db"""

    if not REMOTE_DB_USERNAME or not REMOTE_DB_PASSWORD or not REMOTE_DB_NAME:
        print "Please setup remote db configs"
        return

    if not LOCAL_DB_USERNAME or not LOCAL_DB_PASSWORD or not LOCAL_DB_NAME:
        print "Please setup local db configs"
        return

    with cd("/tmp"):
        run("mysqldump -u%s -p%s %s > latest_db.sql" % (REMOTE_DB_USERNAME,
                                                        REMOTE_DB_PASSWORD,
                                                        REMOTE_DB_NAME))
        run("tar cfz latest_db.sql.tgz latest_db.sql")

    # Download to local
    get("/tmp/latest_db.sql.tgz", "/tmp")

    with lcd("/tmp"):
        local("tar xfz latest_db.sql.tgz")
        local("mysql -u%s -p%s %s < latest_db.sql" % (LOCAL_DB_USERNAME,
                                                      LOCAL_DB_PASSWORD,
                                                      LOCAL_DB_NAME))
