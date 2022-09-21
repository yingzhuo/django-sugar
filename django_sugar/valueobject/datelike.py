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

from dateutil.parser import parse, ParserError

from django_sugar.valueobject import abstractfield


class DateDesc(object):
    """
    日期描述器

    本类型是对日期的包装
    为日期类型提供若干便捷方法
    """

    @staticmethod
    def today():
        return DateDesc(datetime.date.today())

    def __init__(self, date=None, *args, **kwargs):
        if isinstance(date, datetime.datetime):
            self._date = date.date()
        elif isinstance(date, datetime.date):
            self._date = date
        elif isinstance(date, str):
            try:
                defaults = {
                    'fuzzy': True,
                    **kwargs,
                }
                self._date = parse(date, *args, **defaults).date()
            except (OverflowError, ParserError):
                msg = "Cannot parse '%s' as datetime or date." % str(date)
                raise ValueError(msg)
        else:
            self._date = datetime.date.today()

    def __str__(self):
        return str(self._date)

    def __repr__(self):
        return str(self._date)

    def __add__(self, other):
        if isinstance(other, int):
            ndt = self._date + datetime.timedelta(days=other)
            return DateDesc(ndt)
        else:
            raise TypeError('Type not supported.')

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            ndt = self._date - datetime.timedelta(days=other)
            return DateDesc(ndt)
        else:
            raise TypeError('Type not supported.')

    def __isub__(self, other):
        return self.__sub__(other)

    def __gt__(self, other):
        if isinstance(other, DateDesc):
            return self._date > other._date
        if isinstance(other, datetime.datetime):
            return self._date > other.date()
        if isinstance(other, datetime.date):
            return self._date > other
        else:
            raise TypeError('Type not supported.')

    def __ge__(self, other):
        if isinstance(other, DateDesc):
            return self._date >= other._date
        if isinstance(other, datetime.datetime):
            return self._date >= other.date()
        if isinstance(other, datetime.date):
            return self._date >= other
        else:
            raise TypeError('Type not supported.')

    def __lt__(self, other):
        if isinstance(other, DateDesc):
            return self._date < other._date
        if isinstance(other, datetime.datetime):
            return self._date < other.date()
        if isinstance(other, datetime.date):
            return self._date < other
        else:
            raise TypeError('Type not supported.')

    def __le__(self, other):
        if isinstance(other, DateDesc):
            return self._date <= other._date
        if isinstance(other, datetime.datetime):
            return self._date <= other.date()
        if isinstance(other, datetime.date):
            return self._date <= other
        else:
            raise TypeError('Type not supported.')

    def __eq__(self, other):
        if isinstance(other, DateDesc):
            return self._date == other._date
        if isinstance(other, datetime.datetime):
            return self._date == other.date()
        if isinstance(other, datetime.date):
            return self._date == other
        else:
            raise TypeError('Type not supported.')

    def __ne__(self, other):
        if isinstance(other, DateDesc):
            return self._date != other._date
        if isinstance(other, datetime.datetime):
            return self._date != other.date()
        if isinstance(other, datetime.date):
            return self._date != other
        else:
            raise TypeError('Type not supported.')

    @property
    def year(self):
        return self._date.year

    @property
    def year_str(self):
        return str(self._date.year)

    @property
    def month(self):
        return self._date.month

    @property
    def month_str(self):
        return str(self._date.month)

    @property
    def day(self):
        return self._date.day

    @property
    def day_str(self):
        return str(self._date.day)

    @property
    def quarter(self):
        return "%d-Q%d" % (self.year, math.ceil(self.month / 3))

    @property
    def iso_weekday(self):
        return self._date.isoweekday()

    @property
    def week_range_string(self):
        start = self._date - datetime.timedelta(days=self._date.weekday() + 1)
        end = start + datetime.timedelta(days=6)
        return str(start) + '/' + str(end)

    @property
    def in_leap_year(self):
        year = self.year
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

    def astype(self, target_type):
        if target_type == str:
            return str(self)
        elif target_type == int:
            ts = datetime.datetime.combine(self._date, datetime.time()).timestamp()
            return int(ts)
        elif target_type == datetime.datetime:
            return datetime.datetime.combine(self._date, datetime.time())
        elif target_type == datetime.date:
            return self._date
        else:
            raise TypeError('Type not supported.')


# ----------------------------------------------------------------------------------------------------------------------

class DateDescField(abstractfield.AbstractField):
    """
    日期描述器Field

    用于序列化器
    """

    default_error_messages = {
        'invalid': "Invalid string format for 'DateDescriptor'.",
        'past': "DateDescriptor must be past.",
        'future': "DateDescriptor must be future.",
    }

    def __init__(self, *, past=False, future=False, **kwargs):
        self.past = past
        self.future = future
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            dd = DateDesc(data)
            today = DateDesc.today()
            if self.past:
                if dd >= today:
                    self.fail('past')

            if self.future:
                if dd <= today:
                    self.fail('future')

            return dd
        except ValueError:
            self.fail('invalid')
