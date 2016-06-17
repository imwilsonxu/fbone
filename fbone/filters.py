# -*- coding: utf-8 -*-

from datetime import datetime


# http://jinja.pocoo.org/docs/dev/api/#custom-filters
def format_date(value, format='%Y-%m-%d'):
    if value:
        return value.strftime(format)
    else:
        return ""


# https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
def pretty_date(value, default="just now"):
    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default
