# -*- coding: utf-8 -*-

# http://docs.fabfile.org/en/1.5/tutorial.html

import os
from fabric.api import *

#project = "fbone"
#version = "0.1"

# the user to use for the remote commands
#env.user = 'wilson'
# the servers where the commands are executed
env.hosts = ['127.0.0.1']


def run():
    local("python manage.py run")


# alias of run()
def r():
    run()


def initdb():
    local("rm -f /tmp/fbone.sqlite")
    local("python manage.py initdb")


def babel():
    local("python setup.py compile_catalog --directory `find -name translations` --locale zh -f")


def debug():
    initdb()
    run()


# alias of debug()
def d():
    debug()


def init(project="myapp"):
    project_dir = os.getcwd()
    vhost_name = project + ".vhost"
    with cd(project_dir):
        local("sudo chown $USER -R " + project_dir)
        # logs folder
        local("mkdir logs")
        # setup.py and config.py
        local("perl -pi -e 's/\"fbone\"/\"%s\"/g' setup.py fbone/configs/config.py" % project)
        # and *.py
        local("perl -pi -e 's/^from fbone/from %s/g' `find -iname '*.py'`" % project)
        # change fbone/ folder
        local("mv fbone %s" % project)

        # Deploy with mod_wsgi
        # configure wsgi
        local("perl -pi -e 's/fbone/%s/g' app.wsgi MANIFEST.in" % project)
        # configure vhost
        local("perl -pi -e 's!DAEMON_NAME!%s!g' app.vhost" % project)
        local("perl -pi -e 's!PATH_TO_WSGI!%s!g' app.vhost" % os.path.join(project_dir, "app.wsgi"))
        local("perl -pi -e 's!PATH_TO_PROJECT!%s!g' app.vhost" % project_dir)
        local("sudo cp app.vhost /etc/apache2/sites-available/%s" % vhost_name)
        local("sudo a2ensite %s" % vhost_name)
        local("sudo service apache2 reload")

        # virtualenv
        local("virtualenv env")
        activate_this = os.path.join(project_dir, "env/bin/activate_this.py")
        execfile(activate_this, dict(__file__=activate_this))

        # Save downloading time, test only.
        #local("cp -r ~/.virtualenvs/fbone/lib/python2.7/site-packages/ /srv/www/myapp/env/lib/python2.7/")

        # You should move uploads folder to somewhere else
        local("mkdir /tmp/uploads")

        local("python setup.py install")
        local("python manage.py initdb")
        # make db readable
        local("sudo chmod o+w /tmp/%s.sqlite" % project)


def deploy():
    local("virtualenv env")
    activate_this = os.path.join(project_dir, "env/bin/activate_this.py")
    execfile(activate_this, dict(__file__=activate_this))
    local("python setup.py install")
