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
import hashlib


def md5(string, *, charset='utf-8'):
    return hashlib.md5(string.encode(encoding=charset)).hexdigest()


def sha1(string, *, charset='utf-8'):
    return hashlib.sha1(string.encode(encoding=charset)).hexdigest()


def sha224(string, *, charset='utf-8'):
    return hashlib.sha224(string.encode(encoding=charset)).hexdigest()


def sha256(string, *, charset='utf-8'):
    return hashlib.sha256(string.encode(encoding=charset)).hexdigest()


def sha512(string, *, charset='utf-8'):
    return hashlib.sha512(string.encode(encoding=charset)).hexdigest()
