r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import abc
import re

from django_sugar import lang


class PasswordEncoder(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def encode_password(self, raw_password):
        """
        密码原文加密保存

        :param raw_password: 密码原文
        :return: 密码的密文
        """

    def password_matches(self, raw_password, encoded_password):
        """
        比较密码原文和密文是否匹配

        :param raw_password: 密码原文
        :param encoded_password: 密码密文
        :return: 匹配时返回True，否则返回False
        """
        return self.encode_password(raw_password) == encoded_password


class NoopPasswordEncoder(PasswordEncoder):
    ignore_cases = None

    def __init__(self, *, ignore_cases=False):
        if self.ignore_cases is None:
            self.ignore_cases = ignore_cases

    def encode_password(self, raw_password):
        return raw_password

    def password_matches(self, raw_password, encoded_password):
        if self.ignore_cases:
            return raw_password.lower() == encoded_password.lower()
        else:
            return raw_password == encoded_password


class MD4PasswordEncoder(PasswordEncoder):

    def encode_password(self, raw_password):
        return lang.md4(raw_password)


class MD5PasswordEncoder(PasswordEncoder):

    def encode_password(self, raw_password):
        return lang.md5(raw_password)


class SHA1PasswordEncoder(PasswordEncoder):

    def encode_password(self, raw_password):
        return lang.sha1(raw_password)


class SHA256PasswordEncoder(PasswordEncoder):

    def encode_password(self, raw_password):
        return lang.sha256(raw_password)


class SHA512PasswordEncoder(PasswordEncoder):

    def encode_password(self, raw_password):
        return lang.sha512(raw_password)


class SHA224PasswordEncoder(PasswordEncoder):

    def encode_password(self, raw_password):
        return lang.sha224(raw_password)


class Base64PasswordEncoder(PasswordEncoder):

    def encode_password(self, raw_password):
        return lang.base64_urlsafe_encode(raw_password)

    def password_matches(self, raw_password, encoded_password):
        return lang.base64_urlsafe_decode(encoded_password) == raw_password


class ReversePasswordEncoder(PasswordEncoder):

    def encode_password(self, raw_password):
        return raw_password[::-1]


_INNER_ENCODERS = {
    'noop': NoopPasswordEncoder(ignore_cases=False),
    'md4': MD4PasswordEncoder(),
    'md5': MD5PasswordEncoder(),
    'sha1': SHA1PasswordEncoder(),
    'sha256': SHA256PasswordEncoder(),
    'sha512': SHA512PasswordEncoder(),
    'sha224': SHA224PasswordEncoder(),
    'base64': Base64PasswordEncoder(),
    'reverse': ReversePasswordEncoder(),
}

# noinspection PyBroadException
try:
    import bcrypt


    class BcryptPasswordEncoder(PasswordEncoder):

        def encode_password(self, raw_password):
            salt = bcrypt.gensalt(rounds=6)
            byte_array = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
            return str(byte_array, 'utf-8')

        def password_matches(self, raw_password, encoded_password):
            raw_password = raw_password.encode('utf-8')
            encoded_password = encoded_password.encode('utf-8')
            return bcrypt.checkpw(raw_password, encoded_password)


    _INNER_ENCODERS.update(
        {
            'bcrypt': BcryptPasswordEncoder(),
        }
    )

    _BCRYPT_PRESENT = True
except Exception:
    _BCRYPT_PRESENT = False


class DelegatingPasswordEncoder(PasswordEncoder):
    encoding_algorithm = 'bcrypt' if _BCRYPT_PRESENT else 'md5'

    def __len__(self):
        return len(_INNER_ENCODERS)

    def __iter__(self):
        return iter(_INNER_ENCODERS)

    def is_supported(self, alg_name):
        return alg_name in _INNER_ENCODERS

    def encode_password(self, raw_password):
        alg_id = self.encoding_algorithm
        encoder = _INNER_ENCODERS.get(alg_id)
        if encoder is None:
            raise ValueError("alg_id: '%s' not supported." % alg_id)
        return '{%s}%s' % (alg_id, encoder.encode_password(raw_password))

    def password_matches(self, raw_password, encoded_password):
        alg_id, real_encoded_pwd = self._get_alg_and_real_encoded_password(encoded_password)
        encoder = _INNER_ENCODERS.get(alg_id)
        if encoder is None:
            raise ValueError("alg_id: '%s' not supported." % alg_id)
        return encoder.password_matches(raw_password, real_encoded_pwd)

    @staticmethod
    def _get_alg_and_real_encoded_password(encoded_password):
        alg = re.sub(r'^{([a-z0-9_]+)}.*$', r'\1', encoded_password)

        # 不是 '{alg_name}xxx' 格式的密码，当noop处理
        if alg == encoded_password:
            return 'noop', encoded_password
        return alg, re.sub(r'^{[a-z0-9_]+}(.*)$', r'\1', encoded_password)
