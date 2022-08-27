# ----------------------------------------------------------------------------------------------------------------------
#  ____                           ____
# |  _ \(_) __ _ _ __   __ _  ___/ ___| _   _  __ _  __ _ _ __
# | | | | |/ _` | '_ \ / _` |/ _ \___ \| | | |/ _` |/ _` | '__|
# | |_| | | (_| | | | | (_| | (_) |__) | |_| | (_| | (_| | |
# |____// |\__,_|_| |_|\__, |\___/____/ \__,_|\__, |\__,_|_|
#    |__/             |___/                  |___/
#
# https://github.com/yingzhuo/django-sugar
# ----------------------------------------------------------------------------------------------------------------------
import datetime

from django_sugar import lang


class DateRange(lang.PairLike):
    """
    日期范围

    封装一对日期
    """

    _date_1 = None
    _date_2 = None
    _date_format = None
    _delimiter = None
    _dates_list = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        return object.__new__(DateRange)

    def __init__(self, left: datetime.datetime, right: datetime.datetime, **kwargs):
        self._date_format = kwargs.get('date_format', '%Y-%m-%d')
        self._delimiter = kwargs.get('delimiter', '@@')
        self._date_1 = min(left, right)
        self._date_2 = max(left, right)

        self._dates_list = []
        it = self._date_1
        while it <= self._date_2:
            self._dates_list.append(it)
            it = it + datetime.timedelta(days=1)

    def as_list(self):
        return self._dates_list

    def __len__(self):
        return len(self._dates_list)

    def __iter__(self):
        return iter(self.as_list())

    def __str__(self):
        return rf"{self._date_1.strftime(self._date_format)}{self._delimiter}{self._date_2.strftime(self._date_format)}"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self._dates_list[item]

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
            raise TypeError('other type not supported')

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        new_left = self._date_1 - other
        new_right = self._date_2 - other
        return DateRange(new_left, new_right, date_format=self._date_format, delimiter=self._delimiter)

    def __isub__(self, other):
        return self.__sub__(other)

    @property
    def left(self):
        return self._date_1

    @property
    def right(self):
        return self._date_2

    @staticmethod
    def from_string(string: str, *, date_format=None, delimiter=None):
        date_format = date_format or '%Y-%m-%d'
        delimiter = delimiter or '@@'
        parts = string.split(delimiter, 2)
        left = datetime.datetime.strptime(parts[0], date_format)
        right = datetime.datetime.strptime(parts[-1], date_format)
        return DateRange(left, right, date_format=date_format, delimiter=delimiter)

    @staticmethod
    def is_valid_string(string: str, *, date_format=None, delimiter=None):
        try:
            date_format = date_format or '%Y-%m-%d'
            delimiter = delimiter or '@@'
            parts = string.split(delimiter, 2)
            datetime.datetime.strptime(parts[0], date_format)
            datetime.datetime.strptime(parts[-1], date_format)
            return True
        except ValueError:
            return False
