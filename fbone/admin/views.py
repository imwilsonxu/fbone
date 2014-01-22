# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash
from flask.ext.login import login_required

from ..extensions import db
from ..decorators import admin_required

from ..user import User, Role
from .forms import UserForm, RoleForm


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin/index.html', users=users, roles=roles,
                           active='index')


@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='users')

@admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UserForm(obj=user, next=request.args.get('next'))
    form.role_code_select.choices = [(r.name, r.description) for r in Role.query.order_by('name')]

    if form.validate_on_submit():
        form.populate_obj(user)

        user.empty_roles()
        for rolename in form.role_code_select.data:
            user.add_role(rolename)
 
        db.session.add(user)
        db.session.commit()

        flash('User updated.', 'success')
    else:
        form.role_code_select.data = [r.name for r in user.roles]

    return render_template('admin/user.html', user=user, form=form)

@admin.route('/roles')
@login_required
@admin_required
def roles():
    roles = Role.query.all()
    return render_template('admin/roles.html', roles=roles, active='roles')

@admin.route('/role/<int:role_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def role(role_id):
    role = Role.query.filter_by(id=role_id).first_or_404()
    form = RoleForm(obj=role, next=request.args.get('next'))
    if form.validate_on_submit():
        form.populate_obj(role)

        db.session.add(role)
        db.session.commit()

        flash('Role updated.', 'success')

    return render_template('admin/role.html', role=role, form=form)

