# -*- coding: utf-8 -*-

from sqlalchemy import Column

from fbone.extensions import db


class UserStatus(db.Model):

    __tablename__ = 'user_statuses'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, unique=True)
    
    # ================================================================
    # Required by flask-admin
    
    def __unicode__(self):
        return self.name
