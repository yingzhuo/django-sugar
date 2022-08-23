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

import base64 as b


def base64_standard_encode(string, charset='utf-8'):
    string_bytes = string.encode(charset)
    base64_bytes = b.standard_b64encode(string_bytes)
    return base64_bytes.decode(charset)


def base64_standard_decode(base64_string, charset='utf-8'):
    base64_bytes = base64_string.encode(charset)
    string_bytes = b.standard_b64decode(base64_bytes)
    return string_bytes.decode(charset)


def base64_urlsafe_encode(string, charset='utf-8'):
    string_bytes = string.encode(charset)
    base64_bytes = b.urlsafe_b64encode(string_bytes)
    return base64_bytes.decode(charset)


def base64_urlsafe_decode(base64_string, charset='utf-8'):
    base64_bytes = base64_string.encode(charset)
    string_bytes = b.urlsafe_b64decode(base64_bytes)
    return string_bytes.decode(charset)
