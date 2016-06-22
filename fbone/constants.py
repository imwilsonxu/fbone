# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from flask import Markup

ADMIN = 0
STAFF = 1
USER = 2
USER_ROLE = {
    ADMIN: 'admin',
    STAFF: 'staff',
    USER: 'user',
}
USER_ROLE = OrderedDict(sorted(USER_ROLE.items()))

INACTIVE = 0
NEW = 1
ACTIVE = 2
USER_STATUS = {
    INACTIVE: 'inactive',
    NEW: 'new',
    ACTIVE: 'active',
}
USER_STATUS = OrderedDict(sorted(USER_STATUS.items()))

DEFAULT_USER_AVATAR = 'default.jpg'

SEX_TYPES = {
    1: 'Male',
    2: 'Female',
    3: 'Other',
}
SEX_TYPES = OrderedDict(sorted(SEX_TYPES.items()))

INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

ALLOWED_AVATAR_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

USERNAME_LEN_MIN = 4
USERNAME_LEN_MAX = 25
USERNAME_TIP = "Don't worry. you can change it later."

REALNAME_LEN_MIN = 4
REALNAME_LEN_MAX = 25

PASSWORD_LEN_MIN = 6
PASSWORD_LEN_MAX = 16
PASSWORD_TIP = '%s characters or more! Be tricky.' % PASSWORD_LEN_MIN

AGREE_TIP = Markup(
    'Agree to the <a target="blank" href="/terms">Terms of Service</a>')

EMAIL_LEN_MIN = 2
EMAIL_LEN_MAX = 50
EMAIL_TIP = "What's your email address?"

BIO_TIP = "Tell us about yourself"

STRING_LEN = 225
