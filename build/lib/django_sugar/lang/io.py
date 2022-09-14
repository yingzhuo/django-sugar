r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import codecs


def read_file_as_bytes(filename):
    """
    读取二进制文件

    :param filename: 文件
    :return: 字节数组
    """
    with open(filename, 'rb') as f:
        return f.read()


def read_file_as_string(filename, *, charset='utf-8'):
    """
    读取文本文件

    :param filename: 文件
    :param charset: 文件编码
    :return: 文件内容
    """
    with codecs.open(filename, 'r', encoding=charset) as f:
        return f.read()


def read_file_as_lines(filename, *, charset='utf-8'):
    """
    读取文本文件为可迭代的行

    :param filename: 文件
    :param charset: 文件编码
    :return: 文件内容
    """
    with codecs.open(filename, 'r', encoding=charset) as f:
        return [x.rstrip('\n') for x in f.readlines()]
