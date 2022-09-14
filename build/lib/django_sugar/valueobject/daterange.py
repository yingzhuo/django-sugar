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

from django_sugar import assert_type
from django_sugar.valueobject import abstractfield

_DEFAULT_DATETIME_FORMAT = '%Y-%m-%d'
_DEFAULT_DELIMITER = '@@'


class DateRange(object):
    """
    日期范围

    封装一对日期
    """

    _date_1 = None
    _date_2 = None
    _date_format = None
    _delimiter = None

    def __init__(self, left: datetime.datetime, right: datetime.datetime, **kwargs):
        self._date_format = kwargs.get('date_format', _DEFAULT_DATETIME_FORMAT)
        self._delimiter = kwargs.get('delimiter', _DEFAULT_DELIMITER)
        self._date_1 = min(left, right)
        self._date_2 = max(left, right)

    def __iter__(self):
        x = self._date_1
        while x <= self._date_2:
            yield x
            x += datetime.timedelta(days=1)

    def __str__(self):
        return rf"{self._date_1.strftime(self._date_format)}{self._delimiter}{self._date_2.strftime(self._date_format)}"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if isinstance(other, datetime.timedelta):
            new_left = self._date_1 + other
            new_right = self._date_2 + other
            return DateRange(new_left, new_right, date_format=self._date_format, delimiter=self._delimiter)
        elif isinstance(other, DateRange):
            new_left = min(self._date_1, self._date_2, other._date_1, other._date_2)
            new_right = max(self._date_1, self._date_2, other._date_1, other._date_2)
            return DateRange(new_left, new_right, date_format=self._date_format, delimiter=self._delimiter)
        else:
            raise TypeError('type not supported')

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        new_left = self._date_1 - other
        new_right = self._date_2 - other
        return DateRange(new_left, new_right, date_format=self._date_format, delimiter=self._delimiter)

    def __isub__(self, other):
        return self.__sub__(other)

    def __contains__(self, item):
        return self._date_1 <= item <= self._date_2

    @property
    def left(self):
        return self._date_1

    @property
    def right(self):
        return self._date_2

    @staticmethod
    def from_string(string, *, date_format=None, delimiter=None):
        assert_type(string, str)

        try:
            date_format = date_format or _DEFAULT_DATETIME_FORMAT
            delimiter = delimiter or _DEFAULT_DELIMITER
            parts = string.split(delimiter, 2)
            left = datetime.datetime.strptime(parts[0], date_format)
            right = datetime.datetime.strptime(parts[-1], date_format)
            return DateRange(left, right, date_format=date_format, delimiter=delimiter)
        except ValueError:
            msg = "Invalid format for '%s'." % DateRange.__name__
            raise ValueError(msg)

    @staticmethod
    def is_valid_string(string, *, date_format=None, delimiter=None):
        if not isinstance(string, str):
            return False

        try:
            date_format = date_format or _DEFAULT_DATETIME_FORMAT
            delimiter = delimiter or _DEFAULT_DELIMITER
            parts = string.split(delimiter, 2)
            datetime.datetime.strptime(parts[0], date_format)
            datetime.datetime.strptime(parts[-1], date_format)
            return True
        except ValueError:
            return False


# ----------------------------------------------------------------------------------------------------------------------


class DateRangeField(abstractfield.AbstractField):
    """
    DateRange相关Field

    用于序列化器
    """
    date_format = None
    delimiter = None
    default_error_messages = {
        'invalid': "Invalid string format for 'DateRange'.",
    }

    def __init__(self, *, date_format=None, delimiter=None, **kwargs):
        self.date_format = date_format or _DEFAULT_DATETIME_FORMAT
        self.delimiter = delimiter or _DEFAULT_DELIMITER
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not DateRange.is_valid_string(data, date_format=self.date_format, delimiter=self.delimiter):
            self.fail('invalid')
        else:
            return DateRange.from_string(data, date_format=self.date_format, delimiter=self.delimiter)
