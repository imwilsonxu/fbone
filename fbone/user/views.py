# -*- coding: utf-8 -*-

import os

from flask import (Blueprint, render_template, send_from_directory, abort,
                   request, current_app, flash)
from flask import current_app as APP
from flask_login import login_required, current_user

from .forms import ProfileForm, PasswordForm
from .models import User

from ..extensions import db
from ..utils import get_current_time


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<int:user_id>/avatar/<path:filename>')
@login_required
def avatar(user_id, filename):
    dir_path = os.path.join(APP.config['UPLOAD_FOLDER'], 'user_%s' % user_id)
    return send_from_directory(dir_path, filename, as_attachment=True)


@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = ProfileForm(obj=user, email=user.email)

    if form.validate_on_submit():
        form.populate_obj(user)
        user.update_at = get_current_time()
        db.session.commit()

        flash('Public profile updated.', 'success')
    else:
        current_app.logger.debug(form.errors)

    return render_template('user/profile.html', user=user,
            active="profile", form=form)


@user.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = PasswordForm(next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)
        user.password = form.new_password.data

        db.session.add(user)
        db.session.commit()

        flash('Password updated.', 'success')

    return render_template('user/password.html', user=user,
            active="password", form=form)
