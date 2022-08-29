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
from . import *

__version__ = '0.1.0'
__author__ = '应卓'
__author_email__ = 'yingzhor@gmail.com'


# ----------------------------------------------------------------------------------------------------------------------

# 内部使用函数
def assert_type(obj, expected_type, *, assert_error_type=None):
    if not isinstance(obj, expected_type):
        msg = "Incorrect type! Expected type '%s', but got '%s'."
        msg %= (expected_type.__name__, type(obj).__name__)
        assert_error_type = assert_error_type or ValueError
        raise assert_error_type(msg)
