# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, redirect, url_for, send_from_directory
from flask import current_app as APP
from flask.ext.login import login_required, current_user

from .models import User


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
@user.route('/<user_id>/')
@login_required
def index(user_id=None):
    if user_id and user_id != current_user.id:
        return redirect(url_for('user.profile', user_id=user_id))
    return render_template('user/index.html', user=current_user)


@user.route('/<user_id>/')
def profile(user_id):
    user = User.get_by_id(user_id)
    return render_template('user/profile.html', user=user)


@user.route('/<user_id>/avatar/<path:filename>')
@login_required
def avatar(user_id, filename):
    dir_path = os.path.join(APP.config['UPLOAD_FOLDER'], 'user_%s' % user_id)
    return send_from_directory(dir_path, filename, as_attachment=True)
