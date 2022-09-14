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


def ensure_list(obj):
    """
    内部使用函数, 将对象转变成列表(如果有必要的话)

    None -> None
    list -> list
    set -> list
    dict -> list (keys only)
    obj -> [obj]
    """

    if obj is None:
        return None

    if isinstance(obj, str):
        return [obj]

    if isinstance(obj, list):
        return obj

    if isinstance(obj, typing.Iterable):
        return [x for x in obj]

    return [obj]
