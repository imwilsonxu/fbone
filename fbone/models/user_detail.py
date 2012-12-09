# -*- coding: utf-8 -*-

from sqlalchemy import Column

from fbone.extensions import db
from fbone.utils import get_current_time


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
