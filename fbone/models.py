# -*- coding: utf-8 -*-
from sqlalchemy import ( Column, Integer, DateTime, Unicode )
from sqlalchemy.sql import ( select, func )
from sqlalchemy.types import ( TypeDecorator, TEXT )
from sqlalchemy.ext.declarative import ( declared_attr )
from sqlalchemy.ext.mutable import ( Mutable )
from datetime import datetime

from extensions import ( db )
from utils import ( get_current_time )

__all__ = [ 'IdMixin', 'TimestampMixin', 'IdTimestampMixin' ]

class IdMixin(object):
    """
    Provides the :attr:`id` primary key column
    """
    id = db.Column(db.Integer, primary_key=True)
    
class TimestampMixin(object):
    """
    Provides the :attr:`created_at` and :attr:`updated_at` audit timestamps
    """
    created_at = db.Column(db.DateTime, default=get_current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_current_time, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)

    @property
    def deleted(self):
        if self.deleted_at is not None:
            return True
        return False

class IdTimestampMixin(IdMixin, TimestampMixin):
    """
    Base mixin class for all tables that adds id and timestamp columns and includes
    stub :meth:`permissions` and :meth:`url_for` methods
    """
    pass

class TimestampMixin(object):
    """
    Provides the :attr:`created_at` and :attr:`updated_at` audit timestamps
    """
    created_at = db.Column(db.DateTime, default=get_current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_current_time, onupdate=datetime.utcnow, nullable=False)


