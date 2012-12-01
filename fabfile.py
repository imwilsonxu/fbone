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

#def pack():
    #local('rm -rf %s-%s/' % (project, version))
    #local('python setup.py sdist --formats=gztar', capture=False)

# Deploy method form Flask docs. 
# If you don't wanna mess up source codes with deployed codes, pls use this method.
#def deploy():
    #pack()
    ## figure out the release name and version
    #dist = local('python setup.py --fullname', capture=True).strip()

    ## upload the source tarball to the temporary folder on the server
    #put('dist/%s.tar.gz' % dist, '/tmp/%s.tar.gz' % project)

    ## create a place where we can unzip the tarball, then enter
    ## that directory and unzip it
    #run('mkdir /tmp/%s' % project)
    #with cd('/tmp/%s' % project):
        #run('tar xzf /tmp/%s.tar.gz' % project)
    #with cd('/tmp/%s/%s' % (project, dist)):
        ## now setup the package with our virtual environment's
        ## python interpreter
        #run('/var/www/%s/env/bin/python setup.py install' % project)
    ## now that all is set up, delete the folder again
    #run('rm -rf /tmp/%s /tmp/%s.tar.gz' % (project, project))
    ## and finally touch the .wsgi file so that mod_wsgi triggers
    ## a reload of the application
    #run('touch /var/www/%s.wsgi' % project)

def run():
    local("python manage.py run")
    
def initdb():
    local("sudo rm -f /tmp/fbone.sqlite")
    local("python manage.py initdb")

def babel():
    local("python setup.py compile_catalog --directory `find -name translations` --locale zh -f")

def debug():
    babel()
    initdb()
    run()

def init(project="myapp"):
    project_dir = os.getcwd()
    vhost_name = project + ".vhost"
    
    with cd(project_dir):
        local("sudo chmod -R o+w %s" % project_dir)

        # setup.py and config.py
        local("perl -pi -e 's/\"fbone\"/\"%s\"/g' setup.py fbone/config.py" % project)
        # and *.py
        local("perl -pi -e 's/^from fbone/from %s/g' `find -iname '*.py'`" % project)

        # configure wsgi
        local("perl -pi -e 's/fbone/%s/g' app.wsgi MANIFEST.in" % project)

        # change fbone/ folder
        local("mv fbone %s" % project)

        # logs folder
        local("mkdir logs")
        local("sudo chmod -R o+w logs")

        # configure vhost
        local("perl -pi -e 's!DAEMON_NAME!%s!g' app.vhost" % project)
        local("perl -pi -e 's!PATH_TO_WSGI!%s!g' app.vhost" % os.path.join(project_dir, "app.wsgi"))
        local("perl -pi -e 's!PATH_TO_PROJECT!%s!g' app.vhost" % project_dir)
        local("sudo cp app.vhost /etc/apache2/sites-available/%s" % vhost_name)
        #local("sudo a2dissite %s" % vhost_name)
        local("sudo a2ensite %s" % vhost_name)
        local("sudo service apache2 reload")

        # virtualenv
        local("virtualenv env")
        activate_this = os.path.join(project_dir, "env/bin/activate_this.py")
        execfile(activate_this, dict(__file__=activate_this))
        local("python setup.py install")
        local("python manage.py initdb")

        # make db readable to apache
        local("sudo chmod o+w /tmp/%s.sqlite" % project)
