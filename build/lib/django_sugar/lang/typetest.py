r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import typing


def is_callable(obj):
    """
    测试对象是否可调用

    :param obj: 对象
    :return: 结果
    """
    return isinstance(obj, typing.Callable)


def is_collection(obj):
    """
    测试对象是否为collection

    :param obj: 对象
    :return: 结果
    """
    return isinstance(obj, typing.Collection)


def is_iterable(obj):
    """
    测试对象是否为可迭代的

    :param obj: 对象
    :return: 结果
    """
    return isinstance(obj, typing.Iterable)


def is_list(obj):
    """
    测试对象是否为列表

    :param obj: 对象
    :return: 结果
    """
    return isinstance(obj, typing.List)


def is_dict(obj):
    """
    测试对象是否为字典

    :param obj: 对象
    :return: 结果
    """
    return isinstance(obj, typing.Dict)


def is_set(obj):
    """
    测试对象是否为集合

    :param obj: 对象
    :return: 结果
    """
    return isinstance(obj, typing.Set)


def is_tuple(obj):
    """
    测试对象是否为元组

    :param obj: 对象
    :return: 结果
    """
    return isinstance(obj, typing.Tuple)


def is_hashable(obj):
    """
    测试对象是否为可哈希的

    :param obj: 对象
    :return: 结果
    """
    return isinstance(obj, typing.Hashable)


def is_generator(obj):
    """
    测试对象是否为生成器

    :param obj: 对象
    :return: 结果
    """
    return isinstance(obj, typing.Generator)


def is_none(obj):
    """
    测试对象是否为None

    :param obj: 对象
    :return: 结果
    """
    return obj is None
