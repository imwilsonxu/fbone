# -*- coding: utf-8 -*-

from flask.ext.uploads import UploadSet, IMAGES
from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          PasswordField, SubmitField, TextAreaField,
                          ValidationError, required, equal_to, email,
                          length, validators, IntegerField, RadioField,
                          FileField, file_allowed, file_required)
from flask.ext.wtf.html5 import URLField, EmailField, TelField
from flaskext.babel import gettext, lazy_gettext as _
from flask.ext.login import current_user

from fbone.models import User, UserRole


images = UploadSet("images", IMAGES)


class ProfileForm(Form):
    next = HiddenField()
    name = TextField(
            label = _("Username"),
            validators = [
                validators.Required(),
                validators.Length(
                    min = 4,
                    max = 25,
                    ),
                ],
            description = u"Combination of letters/digits/underscore, at least 4 characters.",
            )
    email = EmailField(
            label = _('Email'), 
            validators = [validators.Email(
                message = u"Doesn't look like a valid email."
                )],
            )
    role_id = RadioField(
            label = "Role",
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
                    min = 4,
                    max = 25,
                    ),
                ]
            )
    age = IntegerField(
            label = _('Age'), 
            validators = [
                validators.NumberRange(
                    min=1, 
                    max=200,
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
                required(),
                ]
            )
    new_password = PasswordField(
            label = 'New password', 
            validators = [
                required(), 
                length(
                    min=6, 
                    max=16,
                    )
                ]
            )
    password_again = PasswordField(
            label = 'Password again', 
            validators = [
                required(), 
                length(
                    min=6, 
                    max=16,
                    ), 
                equal_to('new_password'),
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
