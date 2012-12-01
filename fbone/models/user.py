# -*- coding: utf-8 -*-

import os

from werkzeug import (generate_password_hash, check_password_hash,
                      cached_property)
from flask.ext.login import UserMixin

from fbone.extensions import db
from fbone.models import DenormalizedText, UserRole
from fbone.utils import get_current_time


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    role_id = db.Column(db.SmallInteger, nullable=False, default=1)
    avatar = db.Column(db.String)
    #avatar = db.Column(db.String)
    _password = db.Column('password', db.String, nullable=False)
    activation_key = db.Column(db.String)
    followers = db.Column(DenormalizedText)
    following = db.Column(DenormalizedText)
    created_time = db.Column(db.DateTime, default=get_current_time)

    # Relationships
    user_detail = db.relationship("UserDetail", uselist=False, backref="user")

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)
    
    @property
    def role(self):
        return UserRole.filter_by(id=self.role_id).first()

    @property
    def avatar_path(self):
        return os.path.join("img", "users", self.avatar)
    
    @property
    def num_followers(self):
        if self.followers:
            return len(self.followers)
        return 0

    @property
    def num_following(self):
        return len(self.following)

    def follow(self, user):
        user.followers.add(self.id)
        self.following.add(user.id)

    def unfollow(self, user):
        if self.id in user.followers:
            user.followers.remove(self.id)

        if user.id in self.following:
            self.following.remove(user.id)

    def get_following_query(self):
        return User.query.filter(User.id.in_(self.following or set()))

    def get_followers_query(self):
        return User.query.filter(User.id.in_(self.followers or set()))

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(User.name==login,
                                  User.email==login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(
                User.name.ilike(keyword),
                User.email.ilike(keyword),
            ))
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)
