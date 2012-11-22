# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, current_app, g, redirect, url_for, request, flash
from flask.ext.login import login_required, current_user
from flask.ext.wtf import ValidationError
from flaskext.babel import gettext as _

from fbone.extensions import db
from fbone.models import User
from fbone.decorators import keep_login_url
from fbone.forms import ProfileForm, AccountForm


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
    form = ProfileForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        flash(_('Profile updated.'), 'success')
    
    return render_template('settings/profile.html', user=user, active="profile", form=form)


@user.route('/settings/notification')
@login_required
def notification():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    return render_template('settings/notification.html', user=user, active="notification")


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
