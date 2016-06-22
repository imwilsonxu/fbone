# -*- coding: utf-8 -*-

import re
from datetime import datetime
from jinja2 import Markup, escape


def format_date(value, format='%Y-%m-%d'):
    # http://blog.sneawo.com/blog/2015/04/08/strftime-for-datetime-before-1900-year/
    if value:
        return '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(value)
    return ""


# https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
def pretty_date(value, default="just now"):
    now = datetime.utcnow()
    diff = now - value

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


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

def nl2br(value):
    if not value:
        return ""
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                for p in _paragraph_re.split(escape(value.strip())))
    return Markup(result)
