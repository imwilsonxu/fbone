# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    Deploy with apache2 wsgi.
"""

import sys, os, pwd
os.environ['FBONE_APP_CONFIG'] = ''
# http://code.google.com/p/modwsgi/wiki/ApplicationIssues#User_HOME_Environment_Variable
os.environ['HOME'] = pwd.getpwuid(os.getuid()).pw_dir

activate_this = '/var/www/fbone/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

BASE_DIR = os.path.join(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from fbone import create_app
application = create_app()

"""
Deploy Note (Ubuntu):

# Server
sudo mkdir -p /var/www/fbone
sudo chmod -R o+w /var/www/fbone
scp /path/to/this/file /var/www/fbone.wsgi
sudo chmod o+w /var/www/fbone.wsgi

sudo echo "<VirtualHost *:80>
    WSGIDaemonProcess fbone user=wilson group=wilson threads=5
    WSGIScriptAlias / /var/www/fbone.wsgi

    <Directory /var/www/fbone>
        #WSGIScriptReloading On
        WSGIProcessGroup fbone
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>" > /etc/apache2/sites-enabled/fbone

sudo a2ensite fbone.vhost
sudo service apache restart

# Client
fab deploy
"""
