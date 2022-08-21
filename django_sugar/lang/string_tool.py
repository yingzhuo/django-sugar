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
import base64
import uuid


def is_empty(string):
    if string is None:
        return True
    return string == ''


def is_blank(string):
    if string is None:
        return True
    return string.strip() == ''


def empty_to_none(string):
    if is_empty(string):
        return None
    else:
        return string


def blank_to_none(string):
    if is_blank(string):
        return None
    else:
        return string


def none_to_empty(string):
    if string is None:
        return ''
    else:
        return string


# ----------------------------------------------------------------------------------------------------------------------


def base64_standard_encode(string, charset='utf-8'):
    string_bytes = string.encode(charset)
    base64_bytes = base64.standard_b64encode(string_bytes)
    return base64_bytes.decode(charset)


def base64_standard_decode(base64_string, charset='utf-8'):
    base64_bytes = base64_string.encode(charset)
    string_bytes = base64.standard_b64decode(base64_bytes)
    return string_bytes.decode(charset)


def base64_urlsafe_encode(string, charset='utf-8'):
    string_bytes = string.encode(charset)
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    return base64_bytes.decode(charset)


def base64_urlsafe_decode(base64_string, charset='utf-8'):
    base64_bytes = base64_string.encode(charset)
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    return string_bytes.decode(charset)


# ----------------------------------------------------------------------------------------------------------------------


def random_uuid36():
    return str(uuid.uuid4())


def random_uuid32():
    return random_uuid36().replace('-', '')


def random_uuid(*, remove_hyphen=False):
    return random_uuid32() if remove_hyphen else random_uuid36()
