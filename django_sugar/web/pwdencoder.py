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

import bcrypt

from django_sugar import lang

# 支持的加密算法
# 其中reverse算法和noop算法只建议用在开发环境
_SUPPORTED_ALGORITHMS = [
    'noop',
    'bcrypt',
    'md5',
    'sha1',
    'sha256',
    'sha512',
    'base64',
    'reverse',
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


class DelegatingPasswordEncoder(PasswordEncoder):
    # 加密用算法
    encoding_algorithm = 'bcrypt'

    def encode_password(self, raw_password):
        self._check_algorithm()

        if raw_password is None:
            return None

        if self.encoding_algorithm == 'bcrypt':
            salt = bcrypt.gensalt(rounds=6)
            return '{bcrypt}%s' % str(bcrypt.hashpw(raw_password.encode('utf-8'), salt), 'utf-8')

        if self.encoding_algorithm == 'noop':
            return '{noop}%s' % raw_password

        if self.encoding_algorithm == 'md5':
            return '{md5}%s' % lang.md5(raw_password)

        if self.encoding_algorithm == 'sha1':
            return '{sha1}%s' % lang.sha1(raw_password)

        if self.encoding_algorithm == 'sha256':
            return '{sha256}%s' % lang.sha256(raw_password)

        if self.encoding_algorithm == 'sha512':
            return '{sha512}%s' % lang.sha512(raw_password)

        if self.encoding_algorithm == 'reverse':
            return '{reverse}%s' % lang.reverse(raw_password)

        if self.encoding_algorithm == 'base64':
            return '{base64}%s' % lang.base64_urlsafe_encode(raw_password)

        return None

    def password_matches(self, raw_password, encoded_password):
        self._check_algorithm()

        if raw_password is None or encoded_password is None:
            return False

        if encoded_password.startswith('{bcrypt}'):
            encoded_password = encoded_password[len('{bcrypt}'):].encode('utf-8')
            raw_password = raw_password.encode('utf-8')
            return bcrypt.checkpw(raw_password, encoded_password)

        if encoded_password.startswith('{noop}'):
            return encoded_password[len('{noop}'):] == raw_password

        if encoded_password.startswith('{md5}'):
            return encoded_password[len('{md5}'):] == lang.md5(raw_password)

        if encoded_password.startswith('{sha1}'):
            return encoded_password[len('{sha1}'):] == lang.sha1(raw_password)
        if encoded_password.startswith('{sha256}'):
            return encoded_password[len('{sha256}'):] == lang.sha256(raw_password)

        if encoded_password.startswith('{sha512}'):
            return encoded_password[len('{sha512}'):] == lang.sha512(raw_password)

        if encoded_password.startswith('{reverse}'):
            return lang.reverse(encoded_password[len('{reverse}'):]) == raw_password

        if encoded_password.startswith('{base64}'):
            return lang.base64_urlsafe_decode(encoded_password[len('{base64}'):]) == raw_password

        # 默认按明文处理
        return raw_password == encoded_password

    def _check_algorithm(self):
        if self.encoding_algorithm not in _SUPPORTED_ALGORITHMS:
            raise ValueError("'%s' algorithm is not supported")
