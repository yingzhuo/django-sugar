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
import typing


class ChoicesType(object):
    """
    枚举类辅助工具

    作为特质混入到枚举类中
    """

    @classmethod
    def choices(cls):
        if isinstance(cls, typing.Iterable):
            return [(m.name, m.value) for m in cls]
        else:
            raise TypeError("'%s' isn't iterable." % cls.__name__)

    @classmethod
    def contains_name(cls, name):
        if isinstance(cls, typing.Iterable):
            return name in [m.name for m in cls]
        else:
            raise TypeError("'%s' isn't iterable." % cls.__name__)

    @classmethod
    def contains_value(cls, value):
        if isinstance(cls, typing.Iterable):
            return value in [m.value for m in cls]
        else:
            raise TypeError("'%s' isn't iterable." % cls.__name__)

    @classmethod
    def parse_from_name(cls, name):
        if isinstance(cls, typing.Iterable):
            for m in cls:
                if m.name == name:
                    return m
            return None
        else:
            raise TypeError("'%s' isn't iterable." % cls.__name__)

    @classmethod
    def parse_from_value(cls, value):
        if isinstance(cls, typing.Iterable):
            for m in cls:
                if m.value == value:
                    return m
            return None
        else:
            raise TypeError("'%s' isn't iterable." % cls.__name__)

    @classmethod
    def parse(cls, name_or_value):
        if isinstance(cls, typing.Iterable):
            for m in cls:
                if m.name == name_or_value or m.value == name_or_value:
                    return m
        else:
            raise TypeError("'%s' isn't iterable." % cls.__name__)
