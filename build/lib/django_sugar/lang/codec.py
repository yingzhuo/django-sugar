r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import hashlib


def md4(string, *, charset='utf-8'):
    """
    md4哈希

    :param string: 字符串
    :param charset: 字符串encoding字符集
    :return: 结果
    """
    return hashlib.new("md4", string.encode(charset)).hexdigest().lower()


def md5(string, *, charset='utf-8'):
    """
    md5哈希

    :param string: 字符串
    :param charset: 字符串encoding字符集
    :return: 结果
    """
    return hashlib.md5(string.encode(encoding=charset)).hexdigest()


def sha1(string, *, charset='utf-8'):
    """
    sha1哈希

    :param string: 字符串
    :param charset: 字符串encoding字符集
    :return: 结果
    """
    return hashlib.sha1(string.encode(encoding=charset)).hexdigest()


def sha224(string, *, charset='utf-8'):
    """
    sha224哈希

    :param string: 字符串
    :param charset: 字符串encoding字符集
    :return: 结果
    """
    return hashlib.sha224(string.encode(encoding=charset)).hexdigest()


def sha256(string, *, charset='utf-8'):
    """
    sha256哈希

    :param string: 字符串
    :param charset: 字符串encoding字符集
    :return: 结果
    """
    return hashlib.sha256(string.encode(encoding=charset)).hexdigest()


def sha512(string, *, charset='utf-8'):
    """
    sha512哈希

    :param string: 字符串
    :param charset: 字符串encoding字符集
    :return: 结果
    """
    return hashlib.sha512(string.encode(encoding=charset)).hexdigest()
