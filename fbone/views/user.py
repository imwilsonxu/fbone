# -*- coding: utf-8 -*-

import os

from werkzeug import secure_filename

from flask import Blueprint, render_template, current_app, g, redirect, url_for, request, flash
from flask.ext.login import login_required, current_user
from flask.ext.wtf import ValidationError
from flaskext.babel import gettext as _

from fbone.extensions import db
from fbone.models import User
from fbone.decorators import keep_login_url
from fbone.forms import ProfileForm, AccountForm, AvatarForm
from fbone.utils import allowed_file


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
@login_required
def index():
    return render_template('user_index.html', current_user=current_user)


@user.route('/<name>')
def pub(name):
    if current_user.is_authenticated() and current_user.name == name:
        return redirect(url_for('user.index'))

    user = User.query.filter_by(name=name).first_or_404()
    return render_template('user_pub.html', user=user)


@user.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = ProfileForm(
            obj=user.user_detail,
            name = current_user.name,
            email = current_user.email,
            status_id = current_user.status_id,
            role_id = current_user.role_id,
            next = request.args.get('next'),
            )

    if form.validate_on_submit():
        
        form.populate_obj(user)
        form.populate_obj(user.user_detail)

        db.session.add(user)
        db.session.commit()

        flash('Profile updated.', 'success')
    
    return render_template('settings/profile.html', user=user, active="profile", form=form)


@user.route('/settings/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = AccountForm(next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)
        user.activation_key = None
        user.password = form.new_password.data

        db.session.add(user)
        db.session.commit()

        flash(_(form.new_password.data), 'success')
    
    return render_template('settings/account.html', user=user, active="account", form=form)


@user.route('/settings/avatar', methods=['GET', 'POST'])
@login_required
def avatar():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = AvatarForm(
            next = request.args.get('next'),
            )

    if form.validate_on_submit():
        if form.avatar.data:
            file = request.files[form.avatar.name]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                fn, ext = os.path.splitext(filename)
                avatar_filename = os.path.join(current_app.config['USER_IMG_UPLOAD_PATH'], user.name+ext)
                file.save(avatar_filename)
                user.avatar = os.path.join(user.name+ext)
                
                db.session.add(user)
                db.session.commit()
        
                flash('Avatar updated.', 'success')
    
    return render_template('settings/avatar.html', user=user, active="avatar", form=form)
