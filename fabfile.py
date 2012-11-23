# -*- coding: utf-8 -*-

# http://docs.fabfile.org/en/1.5/tutorial.html

from fabric.api import *

project = "fbone"
version = "0.1"

# the user to use for the remote commands
env.user = 'wilson'
# the servers where the commands are executed
env.hosts = ['127.0.0.1']

def pack():
    # create a new source distribution as tarball
    local('rm -rf %s-%s/' % (project, version))
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    pack()
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()

    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/%s.tar.gz' % project)

    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir /tmp/%s' % project)
    with cd('/tmp/%s' % project):
        run('tar xzf /tmp/%s.tar.gz' % project)
    with cd('/tmp/%s/%s' % (project, dist)):
        # now setup the package with our virtual environment's
        # python interpreter
        run('/var/www/%s/env/bin/python setup.py install' % project)
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/%s /tmp/%s.tar.gz' % (project, project))
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    run('touch /var/www/%s.wsgi' % project)

def restart_apache():
    sudo('service apache2 restart')

def ldeploy():
    pack()
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()

    # upload the source tarball to the temporary folder on the server
    local('cp dist/%s.tar.gz /tmp/%s.tar.gz' % (dist, project))

    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    local('mkdir /tmp/%s' % project)
    with lcd('/tmp/%s' % project):
        local('tar xzf /tmp/%s.tar.gz' % project)
    with lcd('/tmp/%s/%s' % (project, dist)):
        # now setup the package with our virtual environment's
        # python interpreter
        local('/var/www/%s/env/bin/python setup.py install' % project)
    # now that all is set up, delete the folder again
    local('rm -rf /tmp/%s /tmp/%s.tar.gz' % (project, project))
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    local('touch /var/www/%s.wsgi' % project)
