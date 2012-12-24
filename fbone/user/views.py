# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, current_app, redirect, url_for, send_from_directory
from flask.ext.login import login_required, current_user

from .models import User
from .constants import DEFAULT_USER_AVATAR


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
@login_required
def index():
    return render_template('user/index.html', current_user=current_user)


@user.route('/<name>')
def pub(name):
    if current_user.is_authenticated() and current_user.name == name:
        return redirect(url_for('user.index'))

    user = User.query.filter_by(name=name).first_or_404()
    return render_template('user/show.html', user=user)


@user.route('/avatar')
@user.route('/avatar/<path:avatar_filename>')
def avatar(avatar_filename=None):
    if avatar_filename is None:
        avatar_filename = DEFAULT_USER_AVATAR
    return send_from_directory(current_app.config['USER_AVATAR_UPLOAD_FOLDER'], avatar_filename)
