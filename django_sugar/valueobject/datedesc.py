r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import datetime
import math


class DateDescriptor(object):
    """
    日期描述器
    """

    def __init__(self, dt):
        self._date = self._ensure_date(dt)
        pass

    def _ensure_date(self, dt):
        if isinstance(dt, datetime.datetime):
            return dt.date()
        elif isinstance(dt, datetime.date):
            return dt
        else:
            raise TypeError("Expect 'datetime.datetime' or 'datetime.date', but got %s", type(dt).__name__)

    def __str__(self):
        return str(self._date)

    def __repr__(self):
        return str(self._date)

    @property
    def year(self):
        return self._date.year

    @property
    def year_str(self):
        return str(self.year)

    @property
    def month(self):
        return self._date.month

    @property
    def month_str(self):
        return '%02d' % self._date.month

    @property
    def day(self):
        return self._date.day

    @property
    def day_str(self):
        return '%02d' % self._date.day

    def is_leap_year(self):
        year = self.year
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

    @property
    def quarter(self):
        return "%d-Q%d" % (self.year, math.ceil(self.month / 3))

    @property
    def iso_weekday(self):
        return self._date.isoweekday()

    def get_weekday_str(self, weekday_mapping=None):
        if not weekday_mapping:
            return self.iso_weekday
        else:
            return weekday_mapping[self.iso_weekday]
