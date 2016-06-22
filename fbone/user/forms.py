# -*- coding: utf-8 -*-

from flask_wtf import Form
from flask_wtf.html5 import URLField, EmailField, TelField

from wtforms import ValidationError, StringField, PasswordField, SubmitField, \
    TextAreaField, FileField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, URL, \
    AnyOf, Optional
from flask_login import current_user

from fbone.user import User
from fbone.constants import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, SEX_TYPES, \
    BIO_TIP, ALLOWED_AVATAR_EXTENSIONS
from fbone.utils import allowed_file


class ProfileForm(Form):
    email = EmailField('Email', [DataRequired(), Email()])
    # Don't use the same name as model because we are going to use populate_obj().
    # avatar_file = FileField("Avatar", [Optional()])
    phone = TelField('Phone', [DataRequired(), Length(max=64)])
    url = URLField('URL', [Optional(), URL()])
    location = StringField('Location', [Optional(), Length(max=64)])
    bio = TextAreaField('Bio', [Optional(), Length(max=1024)],
                        description=BIO_TIP)
    submit = SubmitField('Update profile',
                         render_kw={"class": "btn btn-success"})

    def validate_name(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_name(field.data):
            raise ValidationError("Please pick another name.")

    def validate_avatar_file(form, field):
        if field.data and not allowed_file(field.data.filename):
            raise ValidationError("Please upload files with extensions: %s" %
                                  "/".join(ALLOWED_AVATAR_EXTENSIONS))


class PasswordForm(Form):
    password = PasswordField('Current password', [DataRequired()])
    new_password = PasswordField('New password',
                                 [DataRequired(),
                                  Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField('Password again',
                                   [DataRequired(),
                                    Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX),
                                    EqualTo('new_password')])
    submit = SubmitField('Update password')

    def validate_password(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_password(field.data):
            raise ValidationError("Password is wrong.")
