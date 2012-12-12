# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from fbone.user import User, UserRole, UserStatus, UserDetail
from fbone.extensions import db

from tests import TestCase


class TestUser(TestCase):

    def test_get_current_time(self):

        assert User.query.count() == 2
        assert UserRole.query.count() == 2
        assert UserStatus.query.count() == 4
        assert UserDetail.query.count() == 2
