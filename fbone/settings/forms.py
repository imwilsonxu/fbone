# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import (HiddenField, TextField,
        PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
        FileField, DecimalField, DateField)
from flask.ext.wtf import (Required, Length, EqualTo, Email, AnyOf,
        NumberRange, URL, Optional)
from flask.ext.wtf.html5 import URLField, EmailField, TelField
from flask.ext.login import current_user

from ..user import User, USER_ROLE, USER_STATUS
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX,
        AGE_MIN, AGE_MAX, DEPOSIT_MIN, DEPOSIT_MAX)


class ProfileForm(Form):
    next = HiddenField()
    name = TextField(u'Username', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u'Combination of letters/digits/underscore, at least %s characters.' % USERNAME_LEN_MIN)
    email = EmailField(u'Email', [Required(), Email()])
    # Don't use the same name as model because we are going to use populate_obj().
    avatar_file = FileField(u"Avatar", [Optional()])
    age = IntegerField(u'Age', [Optional(), NumberRange(AGE_MIN, AGE_MAX)])
    phone = TelField(u'Phone', [Optional(), Length(max=64)])
    url = URLField(u'URL', [Optional(), URL()])
    deposit = DecimalField(u'Deposit', [Optional(), NumberRange(DEPOSIT_MIN, DEPOSIT_MAX)])
    location = TextField(u'Location', [Optional(), Length(max=64)])
    bio = TextAreaField(u'Bio', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Save')


class PasswordForm(Form):
    next = HiddenField()
    password = PasswordField('Password', [Required()])
    new_password = PasswordField('New password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField('Password again', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
    submit = SubmitField(u'Save')

    def validate_password(form, field):
        user = User.query.filter_by(name=current_user.name).first()
        if not user.check_password(field.data):
            raise ValidationError("Password is wrong.")
