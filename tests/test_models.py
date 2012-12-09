# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from fbone.models import User, UserDetail, Role, UserStatus
from fbone.extensions import db

from tests import TestCase


class TestUser(TestCase):

    def test_get_current_time(self):

        assert User.query.count() == 2
        assert Role.query.count() == 2
        assert UserStatus.query.count() == 4
        assert UserDetail.query.count() == 2
