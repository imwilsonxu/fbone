# -*- coding: utf-8 -*-
"""
    Misc stuff for working with forms
"""

class FieldDescription(object):
    """
    Holds additional field information for form fields
    """
    def __init__(self, *args, **kwargs):
        self.description = None
        self.placeholder = None
        self.title = None

        if args and len(args) > 0:
            self.description = args[0]

        if kwargs:
            for key,val in kwargs.iteritems():
                if not hasattr(self, key):
                    msg = "'%s' object has no attribute '%s'" % ( self.__class__.__name__, key )
                    raise AttributeError(msg)
                setattr(self, key, val)

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.description

    def __unicode__(self):
        return self.description
