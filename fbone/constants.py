# -*- coding: utf-8 -*-

import os
from collections import OrderedDict

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

JOB_TITLES = {
    1: "CEO",
    2: "CTO",
    3: "COO",
    99: "Other",
}
JOB_TITLES = OrderedDict(sorted(JOB_TITLES.items()))

JOB_TYPES = {
    1: "Full-time",
    2: "Part-time",
    3: "Internship",
    99: "Other",
}
JOB_TYPES = OrderedDict(sorted(JOB_TYPES.items()))

INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

ALLOWED_AVATAR_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

USERNAME_LEN_MIN = 4
USERNAME_LEN_MAX = 25

REALNAME_LEN_MIN = 4
REALNAME_LEN_MAX = 25

PASSWORD_LEN_MIN = 6
PASSWORD_LEN_MAX = 16

AGE_MIN = 1
AGE_MAX = 300

STRING_LEN = 200
