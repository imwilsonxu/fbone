# -*- coding: utf-8 -*-

import os

from werkzeug import secure_filename

from flask import Blueprint, render_template, current_app, g, redirect, url_for, request, flash
from flask.ext.login import login_required, current_user

from ..extensions import db
from ..user import User
from ..decorators import keep_login_url
from ..utils import allowed_file
from .forms import ProfileForm, AccountForm, AvatarForm


settings = Blueprint('settings', __name__, url_prefix='/settings')


@settings.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = ProfileForm(
            obj=user.user_detail,
            name = current_user.name,
            email = current_user.email,
            role_id = current_user.role_id,
            status_id = current_user.status_id,
            next = request.args.get('next'),
            )

    if form.validate_on_submit():
        
        form.populate_obj(user)
        form.populate_obj(user.user_detail)

        db.session.add(user)
        db.session.commit()

        flash('Profile updated.', 'success')
    
    return render_template('settings/profile.html', user=user, active="profile", form=form)


@settings.route('/account', methods=['GET', 'POST'])
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

        flash('Password updated.', 'success')
    
    return render_template('settings/account.html', user=user, active="account", form=form)


@settings.route('/avatar', methods=['GET', 'POST'])
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
