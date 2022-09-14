r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import re

__title__ = 'Django Sugar'
__version__ = '0.1.0'
__author__ = '应卓'
__license__ = 'Apache 2'

# Version synonym
VERSION = __version__


# ----------------------------------------------------------------------------------------------------------------------

def assert_type(obj, expected_type, *, assert_error_type=None):
    """
    断言对象类型

    :param obj: 待测试的对象
    :param expected_type: 指望的类型
    :param assert_error_type: 如果断言失败抛出的异常类型。默认为ValueError
    """
    if not isinstance(obj, expected_type):
        msg = "Incorrect type! Expected type '%s', but got '%s'."
        msg %= (expected_type.__name__, type(obj).__name__)
        assert_error_type = assert_error_type or ValueError
        raise assert_error_type(msg)


def assert_regex_matches(string, regex, *, assert_error_type=None):
    """
    断言字符串是否满足正则表达式

    :param string: 待测试的字符串
    :param regex: 正则表达式
    :param assert_error_type: 如果断言失败抛出的异常类型。默认为ValueError
    """
    assert_error_type = assert_error_type or ValueError
    assert_type(string, str, assert_error_type=assert_error_type)
    if not re.match(regex, string):
        msg = fr"Incorrect string format. Expected pattern: '{regex}'."
        raise assert_error_type(msg)
