# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from fbone.utils import pretty_date

from tests import TestCase


class TestPrettyDate(TestCase):

    def test_func(self):
        days = [
            [timedelta(days=365 * 3), '3 years ago'],
            [timedelta(days=365), '1 year ago'],
            [timedelta(days=30 * 6), '6 months ago'],
            [timedelta(seconds=(60 * 5) + 40), '5 minutes ago'],
        ]
        now = datetime.utcnow()
        for day in days:
            ago = now - day[0]
            assert pretty_date(ago) == day[1]
