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

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class JwtAlgorithmAndKey(object, metaclass=abc.ABCMeta):
    """
    JWT签名算法与加密key
    """

    _algorithm_name = None

    @property
    def algorithm_name(self):
        return self._algorithm_name

    @abc.abstractmethod
    def encoding_secret_key(self):
        pass

    @abc.abstractmethod
    def decoding_secret_key(self):
        pass

    def __str__(self):
        return str(self._algorithm_name)

    def __repr__(self):
        return self.__str__()


class HmacAlgorithm(JwtAlgorithmAndKey):

    def __init__(self, alg_name=None, *, key=None):
        self._algorithm_name = alg_name or 'HS256'
        self._secret_key = key or ('HMACAlgorithm' * 3)[::-1]

    @property
    def encoding_secret_key(self):
        return self._secret_key

    @property
    def decoding_secret_key(self):
        return self._secret_key


class RsaAlgorithm(JwtAlgorithmAndKey):

    def __init__(self, alg_name=None, *, public_key, private_key, passphrase=None):
        if passphrase is not None:
            private_key = serialization.load_pem_private_key(private_key,
                                                             password=passphrase,
                                                             backend=default_backend())
        self._algorithm_name = alg_name or 'RS256'
        self._public_key = public_key
        self._private_key = private_key

    @property
    def encoding_secret_key(self):
        return self._private_key

    @property
    def decoding_secret_key(self):
        return self._public_key
