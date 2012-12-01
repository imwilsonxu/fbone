# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from fbone.models import User, UserDetail
from fbone.extensions import db

from tests import TestCase


class TestUser(TestCase):

    def test_get_current_time(self):
        user = User(
                name = 'tester', 
                email = 'tester@test.com', 
                password = '123456',
                user_detail = UserDetail(
                    real_name = u'Demo Guy',
                    age = 10,
                    url = u'http://demo.example.com', 
                    location = u'Hangzhou', 
                    bio = u'Demo Guy is ... hmm ... just a demo guy.'
                    ),
                )
        db.session.add(user)
        db.session.commit()

        last_created_time = user.created_time
        user.name = 'another_tester'
        db.session.add(user)
        db.session.commit()
        assert user.created_time == last_created_time
