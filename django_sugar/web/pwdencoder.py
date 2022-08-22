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
import abc

from django_sugar.lang import codec

# 支持的加密算法
_SUPPORTED_ALGORITHM = [
    'noop',
    'md5',
    'sha1',
    'sha256',
    'sha512',
]


class PasswordEncoder(object, metaclass=abc.ABCMeta):

    def __new__(cls, *args, **kwargs):
        e = object.__new__(CompositePasswordEncoder)
        e.encoding_algorithm = kwargs.get('encoding_algorithm', 'md5')
        return e

    @abc.abstractmethod
    def encode_password(self, raw_password):
        """
        密码原文加密保存

        :param raw_password: 密码原文
        :return: 密码的密文
        """

    @abc.abstractmethod
    def password_matches(self, raw_password, encoded_password):
        """
        比较密码原文和密文是否匹配

        :param raw_password: 密码原文
        :param encoded_password: 密码密文
        :return: 配置时返回True，否则返回False
        """


class CompositePasswordEncoder(PasswordEncoder):
    encoding_algorithm = None

    def __init__(self, **kwargs):
        if self.encoding_algorithm is None:
            self.encoding_algorithm = kwargs.get('encoding_algorithm', 'md5')

        self._check_algorithm()

    def encode_password(self, raw_password):
        self._check_algorithm()

        if raw_password is None:
            return None

        if self.encoding_algorithm == 'noop':
            return '{noop}%s' % raw_password
        elif self.encoding_algorithm == 'md5':
            return '{md5}%s' % codec.md5(raw_password)
        elif self.encoding_algorithm == 'sha1':
            return '{sha1}%s' % codec.sha1(raw_password)
        elif self.encoding_algorithm == 'sha256':
            return '{sha256}%s' % codec.sha256(raw_password)
        elif self.encoding_algorithm == 'sha512':
            return '{sha512}%s' % codec.sha512(raw_password)
        else:
            pass

    def password_matches(self, raw_password, encoded_password):
        self._check_algorithm()

        if raw_password is None or encoded_password is None:
            return False

        if encoded_password.startswith('{noop}'):
            return encoded_password[len('{noop}'):] == raw_password
        elif encoded_password.startswith('{md5}'):
            return encoded_password[len('{md5}'):] == codec.md5(raw_password)
        elif encoded_password.startswith('{sha1}'):
            return encoded_password[len('{sha1}'):] == codec.sha1(raw_password)
        elif encoded_password.startswith('{sha256}'):
            return encoded_password[len('{sha256}'):] == codec.sha256(raw_password)
        elif encoded_password.startswith('{sha512}'):
            return encoded_password[len('{sha512}'):] == codec.sha512(raw_password)
        else:
            return raw_password == encoded_password

    def _check_algorithm(self):
        if self.encoding_algorithm not in _SUPPORTED_ALGORITHM:
            raise ValueError("'%s' algorithm is not supported")
