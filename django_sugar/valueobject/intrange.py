r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
from django_sugar import assert_type
from django_sugar.valueobject import abstractfield

_DEFAULT_DELIMITER = '@@'


class IntRange(object):
    """
    整数范围
    """
    _int_1 = None
    _int_2 = None
    _delimiter = None

    def __init__(self, left, right, *, delimiter=None):
        self._delimiter = delimiter or _DEFAULT_DELIMITER
        self._int_1 = min(left, right)
        self._int_2 = max(left, right)

    def __str__(self):
        return fr'{self._int_1}{self._delimiter}{self._int_2}'

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(range(self._int_1, self._int_2 + 1))

    def __contains__(self, item):
        return self._int_1 <= item <= self._int_2

    @staticmethod
    def from_string(string, delimiter=None):
        assert_type(string, str)
        delimiter = delimiter or _DEFAULT_DELIMITER
        parts = string.split(delimiter, maxsplit=2)
        return IntRange(
            int(parts[0]),
            int(parts[1]),
            delimiter=delimiter
        )

    @staticmethod
    def is_valid_string(string, delimiter=None):
        try:
            IntRange.from_string(string, delimiter=delimiter)
            return True
        except ValueError:
            return False

    @property
    def left(self):
        return self._int_1

    @property
    def right(self):
        return self._int_2


# ----------------------------------------------------------------------------------------------------------------------


class IntRangeField(abstractfield.AbstractField):
    """
    整数范围相关Field

    用于序列化器
    """
    delimiter = None
    default_error_messages = {
        'invalid': "Invalid string format for 'IntRange'.",
    }

    def __init__(self, *, delimiter, **kwargs):
        self.delimiter = delimiter or _DEFAULT_DELIMITER
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not IntRange.is_valid_string(data):
            self.fail('invalid')
        else:
            return IntRange.from_string(data)
