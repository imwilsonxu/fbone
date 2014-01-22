# -*- coding: utf-8 -*-

from flask import Markup

from flask.ext.wtf import Form
from wtforms import (ValidationError, HiddenField, BooleanField, TextField,
        PasswordField, SubmitField)
from wtforms.validators import Required, Length, EqualTo, Email
from flask.ext.wtf.html5 import EmailField

from ..user import User
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX)

from flask_security import forms

class LoginForm(forms.LoginForm):
    pass


class RecoverPasswordForm(forms.ForgotPasswordForm):
    pass

class ChangePasswordForm(forms.ChangePasswordForm):
    pass

class SignupForm(Form):
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()],
            description=u"What's your email address?")
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s characters or more! Be tricky.' % PASSWORD_LEN_MIN)
    name = TextField(u'Choose your username', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    agree = BooleanField(u'Agree to the ' +
        Markup('<a target="blank" href="/terms">Terms of Service</a>'), [Required()])
    submit = SubmitField('Sign up')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This username is taken')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken')

class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    submit = SubmitField('Reauthenticate')


class OpenIDForm(Form):
    openid = TextField(u'Your OpenID', [Required()])
    submit = SubmitField(u'Log in with OpenID')


class CreateProfileForm(Form):
    openid = HiddenField()
    name = TextField(u'Choose your username', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    email = EmailField(u'Email', [Required(), Email()], description=u"What's your email address?")
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s characters or more! Be tricky.' % PASSWORD_LEN_MIN)
    submit = SubmitField(u'Create Profile')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This username is taken.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken.')
