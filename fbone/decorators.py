# -*- coding: utf-8 -*-

from functools import wraps

from flask import abort
from flask.ext.login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role_code != 0:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
