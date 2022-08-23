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


def is_empty_or_none(string):
    return not string


def is_blank_or_none(string):
    if string is None:
        return True
    return string.strip() == ''


def empty_to_none(string):
    if is_empty_or_none(string):
        return None
    else:
        return string


def blank_to_none(string):
    if is_blank_or_none(string):
        return None
    else:
        return string


def none_to_empty(string):
    if string is None:
        return ''
    else:
        return string
