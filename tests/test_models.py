# -*- coding: utf-8 -*-

from fbone.user import User, UserDetail

from tests import TestCase


class TestUser(TestCase):

    def test_get_current_time(self):

        assert User.query.count() == 2
        assert UserDetail.query.count() == 2
