# -*- coding: utf-8 -*-

import os

from sqlalchemy import Column, types
from werkzeug import generate_password_hash, check_password_hash, cached_property
from flask.ext.login import UserMixin

from ..extensions import db
from ..utils import get_current_time
from .constants import USER, USER_ROLE, INACTIVE, USER_STATUS


class DenormalizedText(types.MutableType, types.TypeDecorator):
    """
    Stores denormalized primary keys that can be
    accessed as a set.

    :param coerce: coercion function that ensures correct
                   type is returned

    :param separator: separator character
    """

    impl = types.Text

    def __init__(self, coerce=int, separator=" ", **kwargs):

        self.coerce = coerce
        self.separator = separator

        super(DenormalizedText, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            items = [str(item).strip() for item in value]
            value = self.separator.join(item for item in items if item)
        return value

    def process_result_value(self, value, dialect):
         if not value:
            return set()
         return set(self.coerce(item) for item in value.split(self.separator))

    def copy_value(self, value):
        return set(value)


class UserDetail(db.Model):

    __tablename__ = 'user_details'

    id = Column(db.Integer, primary_key=True)

    real_name = Column(db.String)
    age = Column(db.Integer)
    phone = Column(db.String)
    url = Column(db.String)
    deposit = Column(db.Numeric)
    location = Column(db.String)
    bio = Column(db.String)

    created_time = Column(db.DateTime, default=get_current_time)
    
    # ================================================================
    # Required by flask-admin
    
    def __unicode__(self):
        return self.real_name


class UserStatus(db.Model):

    __tablename__ = 'user_statuses'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, unique=True)
    
    # ================================================================
    # Required by flask-admin
    
    def __unicode__(self):
        return self.name


class UserRole(db.Model):

    __tablename__ = 'roles'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, unique=True)
    
    # ================================================================
    # Required by flask-admin
    
    def __unicode__(self):
        return self.name


class DenormalizedText(types.MutableType, types.TypeDecorator):
    """
    Stores denormalized primary keys that can be
    accessed as a set.

    :param coerce: coercion function that ensures correct
                   type is returned

    :param separator: separator character
    """

    impl = types.Text

    def __init__(self, coerce=int, separator=" ", **kwargs):

        self.coerce = coerce
        self.separator = separator

        super(DenormalizedText, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            items = [str(item).strip() for item in value]
            value = self.separator.join(item for item in items if item)
        return value

    def process_result_value(self, value, dialect):
         if not value:
            return set()
         return set(self.coerce(item) for item in value.split(self.separator))

    def copy_value(self, value):
        return set(value)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(32), nullable=False, unique=True)
    email = Column(db.String, nullable=False, unique=True)
    activation_key = Column(db.String)
    created_time = Column(db.DateTime, default=get_current_time)

    # ================================================================
    # Avatar
    avatar = Column(db.String)
    @property
    def avatar_path(self):
        return os.path.join("img", "users", self.avatar)
    
    # ================================================================
    # Password
    _password = Column('password', db.String, nullable=False)
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
    
    # ================================================================
    # One-to-many relationship between users and roles.
    role_id = Column(db.SmallInteger, db.ForeignKey("roles.id"), default=USER)
    role = db.relationship('UserRole', backref="users")
    
    def getRole(self):
        return USER_ROLE[self.role_id]
    
    # ================================================================
    # One-to-many relationship between users and user_statuses.
    status_id = Column(db.SmallInteger, db.ForeignKey("user_statuses.id"), default=INACTIVE)
    status = db.relationship('UserStatus', backref="users")

    def getStatus(self):
        return USER_STATUS[self.status_id]

    # ================================================================
    # One-to-one (uselist=False) relationship between users and user_details.
    user_detail_id = Column(db.Integer, db.ForeignKey("user_details.id"))
    user_detail = db.relationship("UserDetail", uselist=False, backref="user")
    
    # ================================================================
    # Follow / Following
    followers = Column(DenormalizedText)
    following = Column(DenormalizedText)
    
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

    # ================================================================
    # Class methods
    
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
    
    # ================================================================
    # Required by flask-admin
    
    def __unicode__(self):
        return self.name
