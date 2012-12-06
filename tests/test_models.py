# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from fbone.models import User, UserDetail, Role
from fbone.extensions import db

from tests import TestCase


class TestUser(TestCase):

    def test_get_current_time(self):

        role_user = Role(name='user')
        user = User(
                name = 'demo', 
                email = 'demo@example.com', 
                password = '123456',
                role = role_user,
                user_detail = UserDetail(
                    real_name = u'Demo Guy',
                    age = 10,
                    url = u'http://demo.example.com', 
                    location = u'Hangzhou', 
                    bio = u'Demo Guy is ... hmm ... just a demo guy.'
                    ),
                )

        role_admin = Role(name='admin')
        admin = User(
                name = 'admin', 
                email = 'admin@example.com', 
                password = '123456',
                role = role_admin,
                user_detail = UserDetail(
                    real_name = u'Admin Guy',
                    age = 20,
                    url = u'http://admin.example.com', 
                    location = u'Mars', 
                    bio = u'Admin Guy is ... hmm ... just a admin guy.'
                    ),
                )
        
        db.session.add(user)
        db.session.add(admin)
        db.session.commit()

        assert User.query.count() == 2
        assert Role.query.count() == 2
        assert UserDetail.query.count() == 2
 
        last_created_time = user.created_time
        user.name = 'another_tester'
        db.session.add(user)
        db.session.commit()
        assert user.created_time == last_created_time
