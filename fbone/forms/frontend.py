# -*- coding: utf-8 -*-

from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          PasswordField, SubmitField, TextField,
                          ValidationError, required, equal_to, email,
                          length)
from flask.ext.wtf.html5 import EmailField
from flaskext.babel import gettext, lazy_gettext as _

from fbone.models import User


class LoginForm(Form):
    next = HiddenField()
    login = TextField('Email', [required()])
    password = PasswordField('Password', [required(), length(min=6, max=16)])
    remember = BooleanField('Remember me')
    submit = SubmitField(_('Sign in'))


class SignupForm(Form):
    next = HiddenField()
    name = TextField(_('Username'), [required()])
    password = PasswordField(_('Password'), [required(), length(min=6, max=16)])
    password_again = PasswordField(_('Password again'), [required(), length(min=6, max=16), equal_to('password')])
    email = EmailField(_('Email'), [required(), email()])
    submit = SubmitField(_('Sign up'))

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError, gettext('This username is taken')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError, gettext('This email is taken')


class RecoverPasswordForm(Form):
    email = EmailField(_('Your email'), validators=[
                      email(message=_('A valid email address is required'))])
    submit = SubmitField(_('Send instructions'))


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField('Password', validators=[
                             required(message=_('Password is required'))])
    password_again = PasswordField(_('Password again'), validators=[
                                   equal_to('password', message=\
                                            _("Passwords don't match"))])
    submit = SubmitField(_('Save'))


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(_('Password'), [required(), length(min=6, max=16)])
    submit = SubmitField(_('Reauthenticate'))
