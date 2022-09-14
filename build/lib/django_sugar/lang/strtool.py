r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""


def ensure_bytes(string_or_bytes, *, charset='utf-8'):
    """
    如有必要，转换成bytes类型

    :param string_or_bytes: 字符串或字节数组
    :param charset: 字符串编码
    :return: 结果
    """
    return string_or_bytes.encode(charset) if isinstance(string_or_bytes, str) else string_or_bytes


def ensure_string(string_or_bytes, *, charset='utf-8'):
    """
    如有必要，转换成str类型

    :param string_or_bytes: 字符串或字节数组
    :param charset: 字符串编码
    :return: 结果
    """
    return str(string_or_bytes, charset) if isinstance(string_or_bytes, bytes) else string_or_bytes


def is_empty_or_none(string):
    """
    判断字符串是否为空串或None

    :param string:
    :return: 结果
    """
    return not string


def is_blank_or_none(string):
    """
    判断字符串是否为空白串或None

    :param string:
    :return: 结果
    """
    if string is None:
        return True
    return string.strip() == ''


def empty_to_none(string):
    """
    空字符串替换为None

    :param string:
    :return: 结果
    """
    if is_empty_or_none(string):
        return None
    else:
        return string


def blank_to_none(string):
    """
    空白字符串替换为None

    :param string:
    :return: 结果
    """
    if is_blank_or_none(string):
        return None
    else:
        return string


def none_to_empty(string):
    """
    None替换成空字符串

    :param string:
    :return: 结果
    """
    if string is None:
        return ''
    else:
        return string


def equals(string1, string2, *, ignore_cases=False):
    """
    比较两个字符串是否相等

    :param string1: 字符串1
    :param string2: 字符串2
    :param ignore_cases: 是否忽略大小写
    :return: 结果
    """
    if ignore_cases:
        return string1.lower() == string2.lower()
    else:
        return string1 == string2


def startswith(string, prefix, *, ignore_cases=False):
    """
    判断字符串是否以指定的前缀开始

    :param string: 字符串
    :param prefix: 前缀
    :param ignore_cases: 是否忽略大小写
    :return: 结果
    """
    if ignore_cases:
        return string.lower().startswith(prefix.lower())
    else:
        return string.startswith(prefix)


def endswith(string, suffix, *, ignore_cases=False):
    """
    判断字符串是否以指定的后缀结束

    :param string: 字符串
    :param suffix: 后缀
    :param ignore_cases: 是否忽略大小写
    :return: 结果
    """
    if ignore_cases:
        return string.lower().endswith(suffix.lower())
    else:
        return string.endswith(suffix)
