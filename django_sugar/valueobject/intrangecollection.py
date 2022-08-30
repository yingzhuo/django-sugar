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
from django_sugar.valueobject import IntRange, abstractfield

_DEFAULT_DELIMITER = ';'
_DELIMITER_OF_INT_RANGE = '@@'


class IntRangeCollection(object):
    """
    整数范围的集合
    """
    _int_range_list = None
    _delimiter = None

    def __init__(self, *, int_range_list, delimiter=None):
        self._delimiter = delimiter or _DEFAULT_DELIMITER
        self._int_range_list = int_range_list

    def __str__(self):
        return self._delimiter.join(map(str, self._int_range_list))

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self._int_range_list)

    def __getitem__(self, item):
        return self._int_range_list[item]

    @staticmethod
    def from_string(string, *, delimiter_of_collection=None, delimiter_of_int_range=None):
        assert_type(string, str)
        delimiter_of_collection = delimiter_of_collection or _DEFAULT_DELIMITER
        delimiter_of_int_range = delimiter_of_int_range or _DELIMITER_OF_INT_RANGE

        parts = string.split(delimiter_of_collection)
        int_range_list = [IntRange.from_string(x, delimiter=delimiter_of_int_range) for x in parts]
        return IntRangeCollection(int_range_list=int_range_list, delimiter=delimiter_of_collection)

    @staticmethod
    def is_valid_string(string, *, delimiter_of_collection=None, delimiter_of_int_range=None):
        try:
            IntRangeCollection.from_string(string,
                                           delimiter_of_collection=delimiter_of_collection,
                                           delimiter_of_int_range=delimiter_of_int_range)
            return True
        except ValueError:
            return False


# ----------------------------------------------------------------------------------------------------------------------

class IntRangeCollectionField(abstractfield.AbstractField):
    """
    整数范围的集合相关Field

    用于序列化器
    """

    default_error_messages = {
        'invalid': "Invalid string format for 'IntRangeCollection'.",
        'max_interval': 'There is a big interval between IntRanges.',
    }
    delimiter_of_collection = None
    delimiter_of_int_range = None
    max_interval = 1

    def __init__(self, delimiter_of_collection=None, delimiter_of_int_range=None, max_interval=1, **kwargs):
        self.delimiter_of_collection = delimiter_of_collection or _DEFAULT_DELIMITER
        self.delimiter_of_int_range = delimiter_of_int_range or _DELIMITER_OF_INT_RANGE
        self.max_interval = max_interval
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        # 检查字符串是否合法
        if not IntRangeCollection.is_valid_string(data,
                                                  delimiter_of_int_range=self.delimiter_of_int_range,
                                                  delimiter_of_collection=self.delimiter_of_collection):
            self.fail('invalid')
        d = IntRangeCollection.from_string(data)

        # 检查间隙问题
        last = None
        for current in d:
            if last is not None:
                if current.left - last.right > self.max_interval:
                    self.fail('max_interval')
            last = current
        return d
