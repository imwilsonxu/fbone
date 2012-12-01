# -*- coding: utf-8 -*-

from fbone.extensions import db


class UserRole(db.Model):

    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    # User: 1
    # Admin: 2
    name = db.Column(db.String)
