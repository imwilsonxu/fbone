# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import ValidationError, HiddenField, BooleanField, StringField, \
                PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.html5 import EmailField

from fbone.user import User
from fbone.constants import USERNAME_LEN_MIN, USERNAME_LEN_MAX, USERNAME_TIP, \
                    PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, PASSWORD_TIP, \
                    EMAIL_LEN_MIN, EMAIL_LEN_MAX, EMAIL_TIP, \
                    AGREE_TIP


class LoginForm(Form):
    next = HiddenField()
    login = StringField('Username or email',
                        [DataRequired(),
                         Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    password = PasswordField('Password',
                             [DataRequired(),
                              Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    remember = BooleanField('Remember me')
    # Use render_kw to set style of submit button
    submit = SubmitField('Sign in',
                         render_kw={"class": "btn btn-success btn-block"})


class SignupForm(Form):
    next = HiddenField()
    email = EmailField(u'Email',
                       [DataRequired(), Email(),
                        Length(EMAIL_LEN_MIN, EMAIL_LEN_MAX)],
                       description=EMAIL_TIP)
    password = PasswordField('Password',
                             [DataRequired(),
                              Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
                             description=PASSWORD_TIP)
    name = StringField('Choose your username',
                       [DataRequired(),
                        Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
                       description=USERNAME_TIP)
    agree = BooleanField(AGREE_TIP, [DataRequired()])
    submit = SubmitField('Sign up',
                         render_kw={"class": "btn btn-success btn-block"})

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This username is taken')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken')


class RecoverPasswordForm(Form):
    email = EmailField(u'Your email',
                       [DataRequired(),
                        Email(),
                        Length(EMAIL_LEN_MIN, EMAIL_LEN_MAX)])
    submit = SubmitField('Send instructions')


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField(u'Password', [DataRequired()])
    password_again = PasswordField(u'Password again',
                                   [EqualTo('password',
                                            message="Passwords don't match")])
    submit = SubmitField('Save')


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(u'Password',
                             [DataRequired(),
                              Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    submit = SubmitField('Reauthenticate')
