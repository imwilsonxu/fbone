# -*- coding: utf-8 -*-

from fbone.extensions import db
from fbone.utils import get_current_time


class UserDetail(db.Model):

    __tablename__ = 'user_details'

    id = db.Column(db.Integer, primary_key=True)

    real_name = db.Column(db.String)
    age = db.Column(db.Integer)
    phone = db.Column(db.String)
    url = db.Column(db.String)
    location = db.Column(db.String)
    bio = db.Column(db.String)

    created_time = db.Column(db.DateTime, default=get_current_time)
    
    # ================================================================
    # Required by flask-admin
    
    def __unicode__(self):
        return self.real_name
