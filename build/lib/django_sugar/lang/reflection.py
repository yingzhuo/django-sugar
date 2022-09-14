r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
from django_sugar import lang


def get_attr(obj, attr_name, *, raise_error=False, error_msg=None):
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        if raise_error:
            msg = error_msg or ("object has no attribute '%s'" % attr_name)
            raise TypeError(msg)
        else:
            return None


def get_callable_attr(obj, attr_name, *, raise_error=False, error_msg=None):
    attr = get_attr(obj, attr_name, raise_error=False)

    if lang.is_callable(attr):
        return attr
    elif raise_error:
        msg = error_msg or ("object has no callable attribute '%s'" % attr_name)
        raise TypeError(msg)
    else:
        return None


def get_attr_names(obj):
    return [x for x in dir(obj) if (not x.startswith('__') and (not x.endswith('__')))]


def get_callable_attr_names(obj):
    ret = []
    for attr_name in get_attr_names(obj):
        attr = getattr(obj, attr_name)
        if lang.is_callable(attr):
            ret.append(attr_name)
    return ret


def get_non_callable_attr_names(obj):
    ret = []
    for attr_name in get_attr_names(obj):
        attr = getattr(obj, attr_name)
        if not lang.is_callable(attr):
            ret.append(attr_name)
    return ret
