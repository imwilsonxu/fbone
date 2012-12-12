# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, ValidationError, validators
from flask.ext.wtf import (HiddenField, BooleanField, TextField,
        PasswordField, SubmitField)
from flask.ext.wtf import Required, Length, EqualTo, Email
from flask.ext.wtf.html5 import EmailField
from flaskext.babel import gettext, lazy_gettext as _

from ..user import User
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, 
        USERNAME_LEN_MIN, USERNAME_LEN_MAX)


class LoginForm(Form):
    next = HiddenField()
    login = TextField(
            'Email', 
            [Required()],
            description = u'Username or email',
            )
    password = PasswordField(
            'Password', 
            [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            )
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class SignupForm(Form):
    next = HiddenField()
    name = TextField(
            'Username', 
            [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            )
    password = PasswordField(
            'Password', 
            [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            )
    password_again = PasswordField(
            'Password again', 
            [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('password')],
            )
    email = EmailField(
            'Email', 
            [Required(), Email()],
            )
    submit = SubmitField('Sign up')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError, gettext('This username is taken')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError, gettext('This email is taken')


class RecoverPasswordForm(Form):
    email = EmailField(
            'Your email', 
            [Email()],
            )
    submit = SubmitField('Send instructions')


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField(
            'Password', 
            [Required()],
            )
    password_again = PasswordField(
            'Password again', 
            [EqualTo('password', message="Passwords don't match")])
    submit = SubmitField('Save')


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(
            'Password', 
            [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            )
    submit = SubmitField('Reauthenticate')
