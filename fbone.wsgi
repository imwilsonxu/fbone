# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    Deploy with apache2 wsgi.
"""

project = "fbone"

import sys, os, pwd
os.environ['%s_APP_CONFIG' % project.upper()] = ''
# http://code.google.com/p/modwsgi/wiki/ApplicationIssues#User_HOME_Environment_Variable
os.environ['HOME'] = pwd.getpwuid(os.getuid()).pw_dir

activate_this = '/var/www/%s/env/bin/activate_this.py' % project
execfile(activate_this, dict(__file__=activate_this))

BASE_DIR = os.path.join(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from fbone import create_app
application = create_app()

#Deploy Note (Ubuntu):

# Server
#sudo mkdir -p /var/www/<project>
#sudo chmod -R o+w /var/www/<project>
#scp /path/to/this/file /var/www/fbone.wsgi
#sudo chmod o+w /var/www/fbone.wsgi

#sudo echo "<VirtualHost *:80>
    #WSGIDaemonProcess <project> user=wilson group=wilson threads=5
    #WSGIScriptAlias / /var/www/fbone.wsgi

    #<Directory /var/www/<project>>
        ##WSGIScriptReloading On
        #WSGIProcessGroup <project>
        #WSGIApplicationGroup %{GLOBAL}
        #Order deny,allow
        #Allow from all
    #</Directory>
#</VirtualHost>" > /etc/apache2/sites-enabled/<project>.vhost

#sudo a2ensite <project>.vhost
#sudo service apache restart

# Client
#fab deploy
