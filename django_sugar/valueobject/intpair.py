r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
from django_sugar.valueobject import abstractfield


class IntPair(object):
    """
    整数对
    """

    def __init__(self, string, sep='@@'):
        try:
            parts = string.split(sep=sep, maxsplit=2)
            n1 = int(parts[0].strip())
            n2 = int(parts[1].strip())
            self._start = min(n1, n2)
            self._end = max(n1, n2)
            self._sep = sep
        except ValueError:
            msg = "'%s' is not a valid string." % string
            raise ValueError(msg)

    def __str__(self):
        return '%d%s%d' % (self._start, self._sep, self._end)

    def __repr__(self):
        return '%d%s%d' % (self._start, self._sep, self._end)

    @property
    def start(self):
        return self._start

    left = start

    @property
    def end(self):
        return self._end

    right = end

    def __iter__(self):
        x = self.start
        while x <= self.end:
            yield x
            x += 1

    def __contains__(self, item):
        return self._start <= item <= self._end

    def __len__(self):
        return self._end - self._start + 1

    def astype(self, target_type, map_func=None):
        if target_type == str:
            return str(self)
        if target_type == list:
            ret = [x for x in self]
            if map_func is not None:
                return list(map(map_func, ret))
            else:
                return ret
        if target_type == set:
            ret = set([x for x in self])
            if map_func is not None:
                return set(map(map_func, ret))
            else:
                return ret

        raise TypeError('Type not supported.')


# ----------------------------------------------------------------------------------------------------------------------

class IntPairField(abstractfield.AbstractField):
    """
    整数范围相关Field

    用于序列化器
    """

    default_error_messages = {
        'invalid': "Invalid string format for 'IntPair'.",
    }

    def __init__(self, sep='@@', *args, **kwargs):
        self._sep = sep
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            return IntPair(data, sep=self._sep)
        except ValueError:
            self.fail('invalid')


# ----------------------------------------------------------------------------------------------------------------------

class IntPairList(object):
    """
    IntPair列表
    """

    def __init__(self, string, sep=';'):
        try:
            self._list = [IntPair(x) for x in string.split(sep=sep)]
            self._sep = sep
        except ValueError:
            msg = "'%s' is not a valid string." % string
            raise ValueError(msg)

    def __iter__(self):
        return iter(self._list)

    def __len__(self):
        return len(self._list)

    def __str__(self):
        return self._sep.join([str(x) for x in self])

    def __repr__(self):
        return self._sep.join([str(x) for x in self])

    def __getitem__(self, item):
        return self._list[item]


# ----------------------------------------------------------------------------------------------------------------------

class IntPairListField(abstractfield.AbstractField):
    """
    IntPair的集合相关Field

    用于序列化器
    """

    default_error_messages = {
        'invalid': "Invalid string format for 'IntPairList'.",
        'max_interval': 'There is a big interval between IntPair.',
    }

    def __init__(self, sep=';', max_interval=None, *args, **kwargs):
        self._sep = sep
        self._max_interval = max_interval
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            ipl = IntPairList(data, sep=self._sep)

            if self._max_interval is not None:
                # 检查间隙问题
                last = None
                for current in ipl:
                    if last is not None:
                        if current.left - last.right > self._max_interval:
                            self.fail('max_interval')
                    last = current

            return ipl
        except ValueError:
            self.fail('invalid')
