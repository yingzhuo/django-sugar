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


def is_callable(obj):
    return isinstance(obj, typing.Callable)


def is_iterable(obj):
    return isinstance(obj, typing.Iterable)


def is_list(obj):
    return isinstance(obj, typing.List)


def is_dict(obj):
    return isinstance(obj, typing.Dict)


def is_set(obj):
    return isinstance(obj, typing.Set)


def is_tuple(obj):
    return isinstance(obj, typing.Tuple)


def is_none(obj):
    return obj is None
