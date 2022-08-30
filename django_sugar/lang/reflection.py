r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
from django_sugar.lang import typetest


def get_attribute(obj, attr_name, *, raise_error=False, error_msg=None):
    try:
        return obj.__getattribute__(attr_name)
    except AttributeError:
        if raise_error:
            msg = error_msg or ("object has no attribute '%s'" % attr_name)
            raise TypeError(msg)
        else:
            return None


def get_callable_attribute(obj, attr_name, *, raise_error=False, error_msg=None):
    attr = get_attribute(obj, attr_name, raise_error=False)

    if typetest.is_callable(attr):
        return attr
    elif raise_error:
        msg = error_msg or ("object has no callable attribute '%s'" % attr_name)
        raise TypeError(msg)
    else:
        return None
