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

from django_sugar.valueobject import abstractfield


class DateDescriptor(object):
    """
    日期描述器
    """

    @staticmethod
    def today():
        return DateDescriptor(datetime.date.today())

    @staticmethod
    def from_string(string, *, date_format='%Y-%m-%d'):
        dt = datetime.datetime.strptime(string, date_format)
        return DateDescriptor(dt)

    @staticmethod
    def is_valid_string(string, *, date_format='%Y-%m-%d'):
        try:
            DateDescriptor.from_string(string, date_format=date_format)
            return True
        except ValueError:
            return False

    def __init__(self, dt):
        self._date = self._ensure_date(dt)

    @property
    def date(self):
        return self._date

    @property
    def datetime(self):
        return datetime.datetime.combine(self._date, datetime.time())

    def _ensure_date(self, dt):
        if isinstance(dt, datetime.datetime):
            return dt.date()
        elif isinstance(dt, datetime.date):
            return dt
        else:
            msg = "Incorrect type! Expected type 'datetime.datetime' or 'datetime.date', but got '%s'" % \
                  type(dt).__name__
            raise TypeError(msg)

    def __str__(self):
        return str(self._date)

    def __repr__(self):
        return str(self._date)

    def __add__(self, other):
        if isinstance(other, int):
            new_date = self._date + datetime.timedelta(days=other)
            return DateDescriptor(new_date)
        else:
            raise TypeError('type not supported')

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            new_date = self._date - datetime.timedelta(days=other)
            return DateDescriptor(new_date)
        else:
            raise TypeError('type not supported')

    def __isub__(self, other):
        return self.__sub__(other)

    def __gt__(self, other):
        if isinstance(other, DateDescriptor):
            return self._date > other._date
        else:
            raise TypeError('type not supported')

    def __ge__(self, other):
        if isinstance(other, DateDescriptor):
            return self._date >= other._date
        else:
            raise TypeError('type not supported')

    def __lt__(self, other):
        if isinstance(other, DateDescriptor):
            return self._date < other._date
        else:
            raise TypeError('type not supported')

    def __le__(self, other):
        if isinstance(other, DateDescriptor):
            return self._date <= other._date
        else:
            raise TypeError('type not supported')

    def __eq__(self, other):
        if isinstance(other, DateDescriptor):
            return self._date == other._date
        else:
            raise TypeError('type not supported')

    def __ne__(self, other):
        if isinstance(other, DateDescriptor):
            return self._date != other._date
        else:
            raise TypeError('type not supported')

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


# ----------------------------------------------------------------------------------------------------------------------

class DateDescriptorField(abstractfield.AbstractField):
    """
    日期描述器Field

    用于序列化器
    """

    default_error_messages = {
        'invalid': "Invalid string format for 'DateDescriptor'",
    }

    def __init__(self, *, date_format='%Y-%m-%d', **kwargs):
        self.date_format = date_format
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not DateDescriptor.from_string(data, date_format=self.date_format):
            self.fail('invalid')
        else:
            return DateDescriptor.from_string(data, date_format=self.date_format)
