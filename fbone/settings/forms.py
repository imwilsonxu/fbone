# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, ValidationError, validators
from flask.ext.wtf import (HiddenField, BooleanField, TextField,
        PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
        FileField, DecimalField, DateField)
from flask.ext.wtf import (Required, Length, EqualTo, Email, AnyOf, 
        NumberRange, URL)
from flask.ext.wtf.html5 import URLField, EmailField, TelField
from flaskext.babel import gettext, lazy_gettext as _
from flask.ext.login import current_user

from ..user import User, USER_ROLE, USER_STATUS
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, 
        USERNAME_LEN_MIN, USERNAME_LEN_MAX, REALNAME_LEN_MIN, 
        REALNAME_LEN_MAX, AGE_MIN, AGE_MAX, DEPOSIT_MIN, DEPOSIT_MAX)


class ProfileForm(Form):
    next = HiddenField()
    name = TextField(
            label = _("Username"),
            validators = [
                Required(),
                Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX),
                ],
            description = u"Combination of letters/digits/underscore, at least %s characters." % USERNAME_LEN_MIN,
            )
    email = EmailField(
            label = _('Email'), 
            validators = [Email()],
            )
    created_time = DateField(
            label = _('Created time'),
            )
    role_id = RadioField(
            label = "Role",
            validators = [AnyOf([str(val) for val in USER_ROLE.keys()])],
            choices = [(str(val), label) for val, label in USER_ROLE.items()],
            )
    status_id = RadioField(
            label = "Status",
            validators = [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices = [(str(val), label) for val, label in USER_STATUS.items()],
            )
    real_name = TextField(
            label = _('Real name'),
            validators = [
                Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX),
                ]
            )
    age = IntegerField(
            label = _('Age'), 
            validators = [NumberRange(AGE_MIN, AGE_MAX)],
            )
    phone = TelField(
            label = _('Phone'), 
            )
    url = URLField(
            label = _('URL'), 
            validators = [URL()],
            )
    deposit = DecimalField(
            label = _('Deposit'), 
            validators = [NumberRange(DEPOSIT_MIN, DEPOSIT_MAX)],
            )
    location = TextField(
            label = _('Location'), 
            validators = [Length(max=50)]
            )
    bio = TextAreaField(
            label = _('Bio'), 
            validators = [Length(max=1024)]
            )
    submit = SubmitField(_('Save'))


class AccountForm(Form):
    next = HiddenField()
    password = PasswordField(
            label = 'Password', 
            validators = [Required()]
            )
    new_password = PasswordField(
            label = 'New password', 
            validators = [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            )
    password_again = PasswordField(
            label = 'Password again', 
            validators = [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')]
            )
    submit = SubmitField(_('Save'))

    def validate_password(form, field):
        user = User.query.filter_by(name=current_user.name).first()
        if not user.check_password(field.data):
             raise ValidationError("Password is wrong.")


class AvatarForm(Form):
    next = HiddenField()
    avatar = FileField(
            label = _("Username"),
            validators = [Required()]
            )
    submit = SubmitField(_('Save'))
