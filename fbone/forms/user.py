# -*- coding: utf-8 -*-

from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          PasswordField, SubmitField, TextAreaField,
                          ValidationError, required, equal_to, email,
                          length, validators)
from flaskext.babel import gettext, lazy_gettext as _
from flask.ext.login import current_user

from fbone.models import User


class ProfileForm(Form):
    next = HiddenField()
    name = TextField(_('Username'))
    email = TextField(_('email'), [validators.Email()])
    website = TextField(_('URL'), [validators.URL()])
    location = TextField(_('Location'), [validators.Length(max=100)])
    bio = TextAreaField(_('bio'), [validators.Length(max=200)])
    submit = SubmitField(_('Save'))


class AccountForm(Form):
    next = HiddenField()
    password = PasswordField(_('Password'), [required()])
    new_password = PasswordField(_('New password'), [required(), length(min=6, max=16)])
    password_again = PasswordField(_('Password again'), [required(), length(min=6, max=16), equal_to('new_password')])
    submit = SubmitField(_('Save'))

    def validate_password(form, field):
        user = User.query.filter_by(name=current_user.name).first()
        if not user.check_password(field.data):
             raise ValidationError(_("Password is wrong."))
