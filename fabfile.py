# -*- coding: utf-8 -*-

from fabric.api import *

# the user to use for the remote commands
env.user = 'user_of_deploy_machine'
# the servers where the commands are executed
env.hosts = ['ip_of_deploy_machine']

def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    pack()
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/fbone.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir /tmp/fbone')
    with cd('/tmp/fbone'):
        run('tar xzf /tmp/fbone.tar.gz')
    with cd('/tmp/fbone/%s' % dist):
        # now setup the package with our virtual environment's
        # python interpreter
        run('/var/www/fbone/env/bin/python setup.py install')
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/fbone /tmp/fbone.tar.gz')
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    run('touch /var/www/fbone.wsgi')
