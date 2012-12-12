# -*- coding: utf-8 -*-

import os

from werkzeug import secure_filename

from flask import Blueprint, render_template, current_app, g, redirect, url_for
from flask.ext.login import login_required, current_user

from .models import User


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
