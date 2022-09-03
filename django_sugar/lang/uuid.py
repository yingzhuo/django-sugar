r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import uuid as u


def random_uuid36():
    """
    生成随机UUID

    :return: uuid
    """
    return str(u.uuid4())


def random_uuid32():
    """
    生成随机UUID (移除了'-'符号)

    :return: uuid
    """
    return random_uuid36().replace('-', '')


def random_uuid(*, remove_hyphen=False):
    """
    生成随机UUID

    :param remove_hyphen: 是否要移除结果中的'-'符号
    :return: uuid
    """
    return random_uuid32() if remove_hyphen else random_uuid36()
