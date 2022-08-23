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
import random as r
import string as s


def random_string(length, *, chars):
    if length < 1:
        return ''
    return ''.join(r.choice(chars) for _ in range(length))


def ascii_letters(length):
    return random_string(length, chars=s.ascii_letters)


def lowercase_letters(length):
    return random_string(length, chars=s.ascii_lowercase)


def uppercase_letters(length):
    return random_string(length, chars=s.ascii_uppercase)


def digits_letters(length):
    return random_string(length, chars=s.digits)
