r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import importlib


def is_module_available(module_name):
    """
    测试是否能加载制定的模块

    :param module_name: 待测试的模块名称
    :return: 测试结果
    """
    # 只考虑Python3.4之后的版本
    return importlib.util.find_spec(module_name) is not None
