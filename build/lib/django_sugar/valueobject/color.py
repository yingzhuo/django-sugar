r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
from django_sugar import assert_type, assert_regex_matches
from django_sugar.valueobject import abstractfield


class Color(object):
    """
    颜色
    """

    _red = None
    _green = None
    _blue = None

    def __init__(self, r, g, b):
        if not (r >= 0 and g >= 0 and b >= 0):
            raise ValueError('Value out of range. Must be between 0 and 255.')
        if not (r <= 255 and g <= 255 and b <= 255):
            raise ValueError('Value out of range. Must be between 0 and 255.')
        self._red, self._green, self._blue = r, g, b

    @property
    def r(self):
        return self._red

    @property
    def g(self):
        return self._green

    @property
    def b(self):
        return self._blue

    def __iter__(self):
        return iter((self._red, self._green, self._blue))

    @staticmethod
    def from_string(string):
        assert_type(string, str)
        assert_regex_matches(string, r'^rgb\([0-9]+,[ ]*[0-9]+,[ ]*[0-9]+\)$')
        parts = string.lstrip('rgb(').rstrip(')').split(',', maxsplit=3)
        return Color(int(parts[0]), int(parts[1]), int(parts[2]))

    @staticmethod
    def is_valid_string(string):
        try:
            Color.from_string(string)
            return True
        except ValueError:
            return False

    def __str__(self):
        return "rgb(%d,%d,%d)" % (self._red, self._green, self._blue)

    def __repr__(self):
        return self.__str__()


# ----------------------------------------------------------------------------------------------------------------------

class ColorField(abstractfield.AbstractField):
    """
    颜色Field

    用于序列化器
    """

    default_error_messages = {
        'invalid': "Invalid string format for 'Color'.",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not Color.is_valid_string(data):
            self.fail('invalid')
        else:
            return Color.from_string(data)
