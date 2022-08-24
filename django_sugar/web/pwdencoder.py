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

from django_sugar.lang import codec, strtool, base64

# 支持的加密算法
# 其中reverse算法和noop算法只建议用在开发环境
_SUPPORTED_ALGORITHMS = [
    'noop',
    'reverse',
    'md5',
    'sha1',
    'sha256',
    'sha512',
    'base64',
]


class PasswordEncoder(object, metaclass=abc.ABCMeta):

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
    encoding_algorithm = 'md5'

    def encode_password(self, raw_password):
        self._check_algorithm()

        if raw_password is None:
            return None

        if self.encoding_algorithm == 'noop':
            return '{noop}%s' % raw_password

        if self.encoding_algorithm == 'md5':
            return '{md5}%s' % codec.md5(raw_password)

        if self.encoding_algorithm == 'sha1':
            return '{sha1}%s' % codec.sha1(raw_password)

        if self.encoding_algorithm == 'sha256':
            return '{sha256}%s' % codec.sha256(raw_password)

        if self.encoding_algorithm == 'sha512':
            return '{sha512}%s' % codec.sha512(raw_password)

        if self.encoding_algorithm == 'reverse':
            return '{reverse}%s' % strtool.reverse(raw_password)

        if self.encoding_algorithm == 'base64':
            return '{base64}%s' % base64.base64_urlsafe_encode(raw_password)

        return None

    def password_matches(self, raw_password, encoded_password):
        self._check_algorithm()

        if raw_password is None or encoded_password is None:
            return False

        if encoded_password.startswith('{noop}'):
            return encoded_password[len('{noop}'):] == raw_password

        if encoded_password.startswith('{md5}'):
            return encoded_password[len('{md5}'):] == codec.md5(raw_password)

        if encoded_password.startswith('{sha1}'):
            return encoded_password[len('{sha1}'):] == codec.sha1(raw_password)
        if encoded_password.startswith('{sha256}'):
            return encoded_password[len('{sha256}'):] == codec.sha256(raw_password)

        if encoded_password.startswith('{sha512}'):
            return encoded_password[len('{sha512}'):] == codec.sha512(raw_password)

        if encoded_password.startswith('{reverse}'):
            return strtool.reverse(encoded_password[len('{reverse}'):]) == raw_password

        if encoded_password.startswith('{base64}'):
            return base64.base64_urlsafe_decode(encoded_password[len('{base64}'):]) == raw_password

        # 默认按明文处理
        return raw_password == encoded_password

    def _check_algorithm(self):
        if self.encoding_algorithm not in _SUPPORTED_ALGORITHMS:
            raise ValueError("'%s' algorithm is not supported")
