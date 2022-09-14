r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import random as r
import string as s


def random_string(length, *, chars):
    """
    生成随机字符串

    :param length: 要生成的字符串长度
    :param chars: 可选的字符集合 (string)
    :return: 随机字符串
    """
    if length < 1:
        return ''
    return ''.join(r.choice(chars) for _ in range(length))


def random_ascii_letters(length):
    """
    生成ASCII随机字符串

    :param length: 要生成的字符串长度
    :return: 随机字符串
    """
    return random_string(length, chars=s.ascii_letters)


def random_lowercase_letters(length):
    """
    生成ASCII小写字母随机字符串

    :param length: 要生成的字符串长度
    :return: 随机字符串
    """
    return random_string(length, chars=s.ascii_lowercase)


def random_uppercase_letters(length):
    """
    生成ASCII大写字母随机字符串

    :param length: 要生成的字符串长度
    :return: 随机字符串
    """
    return random_string(length, chars=s.ascii_uppercase)


def random_digits_letters(length):
    """
    生成数字字符字母随机字符串

    :param length: 要生成的字符串长度
    :return: 随机字符串
    """
    return random_string(length, chars=s.digits)


def random_printable_letters(length):
    """
    生成可打印字符字母随机字符串

    :param length: 要生成的字符串长度
    :return: 随机字符串
    """
    return random_string(length, chars=s.printable)


def random_integer(left, right):
    """
    生成随机数字

    :param left: 区间左值 (包含)
    :param right: 区间右值 (包含)
    :return: 随机整数
    """
    return r.randint(left, right)


def random_boolean():
    """
    生成随机布尔值

    :return: 随机布尔值
    """
    return bool(r.getrandbits(1))
