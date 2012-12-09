# -*- coding: utf-8 -*-

from wtforms.fields import (HiddenField, BooleanField, TextField,
        PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
        FileField, DecimalField, DateField)
from flask.ext.wtf import Form, ValidationError, validators
from flask.ext.wtf.html5 import URLField, EmailField, TelField
from flaskext.babel import gettext, lazy_gettext as _
from flask.ext.login import current_user

from fbone.models import User, Role
from fbone.utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, 
        USERNAME_LEN_MIN, USERNAME_LEN_MAX, REALNAME_LEN_MIN, 
        REALNAME_LEN_MAX, AGE_MIN, AGE_MAX, DEPOSIT_MIN, DEPOSIT_MAX)


class ProfileForm(Form):
    next = HiddenField()
    name = TextField(
            label = _("Username"),
            validators = [
                validators.Required(),
                validators.Length(
                    min = USERNAME_LEN_MIN,
                    max = USERNAME_LEN_MAX,
                    ),
                ],
            description = u"Combination of letters/digits/underscore, at least %s characters." % USERNAME_LEN_MIN,
            )
    email = EmailField(
            label = _('Email'), 
            validators = [validators.Email(
                message = u"Doesn't look like a valid email."
                )],
            )
    created_time = DateField(
            label = _('Created time'),
            )
    role_id = RadioField(
            label = "Role",
            # TODO: don't hardcode roles.
            validators = [
                validators.AnyOf(["1", "2"]),
                ],
            choices = [
                ("1", "user"),
                ("2", "admin"),
                ],
            )
    real_name = TextField(
            label = _('Real name'),
            validators = [
                validators.Length(
                    min = REALNAME_LEN_MIN,
                    max = REALNAME_LEN_MAX,
                    ),
                ]
            )
    age = IntegerField(
            label = _('Age'), 
            validators = [
                validators.NumberRange(
                    min = AGE_MIN, 
                    max = AGE_MAX,
                    ),
                ],
            )
    phone = TelField(
            label = _('Phone'), 
            )
    url = URLField(
            label = _('URL'), 
            validators = [
                validators.URL(),
                ],
            )
    deposit = DecimalField(
            label = _('Deposit'), 
            validators = [
                validators.NumberRange(
                    min = DEPOSIT_MIN, 
                    max = DEPOSIT_MAX,
                    ),
                ],
            )
    location = TextField(
            label = _('Location'), 
            validators = [
                validators.Length(
                    max=50,
                    ),
                ]
            )
    bio = TextAreaField(
            label = _('Bio'), 
            validators = [
                validators.Length(
                    max=1024,
                    ),
                ]
            )
    submit = SubmitField(_('Save'))


class AccountForm(Form):
    next = HiddenField()
    password = PasswordField(
            label = 'Password', 
            validators = [
                validators.Required(),
                ]
            )
    new_password = PasswordField(
            label = 'New password', 
            validators = [
                validators.Required(), 
                validators.Length(
                    min = PASSWORD_LEN_MIN, 
                    max = PASSWORD_LEN_MAX,
                    )
                ],
            )
    password_again = PasswordField(
            label = 'Password again', 
            validators = [
                validators.Required(), 
                validators.Length(
                    min = PASSWORD_LEN_MIN, 
                    max = PASSWORD_LEN_MAX,
                    ), 
                validators.EqualTo('new_password'),
                ]
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
            validators = [
                validators.Required(),
                ]
            )
    submit = SubmitField(_('Save'))
