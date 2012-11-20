# -*- coding: utf-8 -*-

from werkzeug import (generate_password_hash, check_password_hash,
                      cached_property)
from flask.ext.login import UserMixin

from fbone.extensions import db
from fbone.models import DenormalizedText
from fbone.utils import get_current_time, VARCHAR_LEN_128


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(VARCHAR_LEN_128), nullable=False, unique=True)
    email = db.Column(db.String(VARCHAR_LEN_128), nullable=False, unique=True)
    _password = db.Column('password', db.String(VARCHAR_LEN_128), nullable=False)
    activation_key = db.Column(db.String(VARCHAR_LEN_128))
    followers = db.Column(DenormalizedText)
    following = db.Column(DenormalizedText)
    created_time = db.Column(db.DateTime, default=get_current_time)

    def __repr__(self):
        return '<User %r>' % self.name

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
