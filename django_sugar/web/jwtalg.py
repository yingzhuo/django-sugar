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

from django_sugar import lang


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
    """
    HMAC签名算法
    """

    def __init__(self, alg_name=None, *, key):
        alg_name = alg_name or 'HS256'
        if alg_name not in {'HS256', 'HS384', 'HS512'}:
            raise ValueError(f"Algorithm '{alg_name} not supported.")

        self._algorithm_name = alg_name
        self._secret_key = key

    @property
    def encoding_secret_key(self):
        return self._secret_key

    @property
    def decoding_secret_key(self):
        return self._secret_key


class RsaAlgorithm(JwtAlgorithmAndKey):
    """
    RSA签名算法

    提示:
        生成密钥文件 (without passphrase):
        openssl genrsa -out rsa_private.key 2048
        openssl rsa -in rsa_private.key -pubout -out rsa_public.key

        生成密钥文件 (with passphrase)
        openssl genrsa -aes256 -passout pass:<passphrase> -out rsa_aes_private.key 2048
        openssl rsa -in rsa_aes_private.key -passin pass:<passphrase> -pubout -out rsa_public.key

    参考:
        https://www.wpoven.com/tools/
    """

    def __init__(self, alg_name=None, *, public_key, private_key, passphrase=None):
        alg_name = alg_name or 'RS256'
        if alg_name not in {'RS256', 'RS384', 'RS512', 'PS256', 'PS384', 'PS512'}:
            raise ValueError(f"Algorithm '{alg_name} not supported.")

        public_key = lang.ensure_bytes(public_key)
        private_key = lang.ensure_bytes(private_key)
        passphrase = lang.ensure_bytes(passphrase)

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


class EcdsaAlgorithm(JwtAlgorithmAndKey):
    """
    ECDSA签名算法

    提示:
        生成密钥文件:
        openssl ecparam -name prime256v1 -genkey -noout -out ecdsa_private.key
        openssl ec -in ecdsa_private.key -pubout -out ecdsa_public.key

    参考:
        https://www.wpoven.com/tools/
    """

    def __init__(self, alg_name=None, *, public_key, private_key, passphrase=None):
        alg_name = alg_name or 'ES256K'
        if alg_name not in {'ES256', 'ES256K', 'ES384', 'ES521', 'ES512'}:
            raise ValueError(f"Algorithm '{alg_name} not supported.")

        public_key = lang.ensure_bytes(public_key)
        private_key = lang.ensure_bytes(private_key)
        passphrase = lang.ensure_bytes(passphrase)

        if passphrase is not None:
            private_key = serialization.load_pem_private_key(private_key,
                                                             password=passphrase,
                                                             backend=default_backend())

        self._algorithm_name = alg_name
        self._public_key = public_key
        self._private_key = private_key

    @property
    def encoding_secret_key(self):
        return self._private_key

    @property
    def decoding_secret_key(self):
        return self._public_key


class NoneAlgorithm(JwtAlgorithmAndKey):
    """
    无签名算法
    """

    _algorithm_name = 'none'

    @property
    def encoding_secret_key(self):
        return None

    @property
    def decoding_secret_key(self):
        return None


# ----------------------------------------------------------------------------------------------------------------------

def create_none_algorithm():
    return NoneAlgorithm()


def create_hs256_algorithm(key: str):
    return HmacAlgorithm('HS256', key=key)


def create_hs384_algorithm(key: str):
    return HmacAlgorithm('HS384', key=key)


def create_hs512_algorithm(key: str):
    return HmacAlgorithm('HS512', key=key)


def create_rs256_algorithm(public_key, private_key, passphrase=None):
    return RsaAlgorithm('RS256', public_key=public_key, private_key=private_key, passphrase=passphrase)


def create_rs384_algorithm(public_key, private_key, passphrase=None):
    return RsaAlgorithm('RS384', public_key=public_key, private_key=private_key, passphrase=passphrase)


def create_rs512_algorithm(public_key, private_key, passphrase=None):
    return RsaAlgorithm('RS512', public_key=public_key, private_key=private_key, passphrase=passphrase)


def create_ps256_algorithm(public_key, private_key, passphrase=None):
    return RsaAlgorithm('PS256', public_key=public_key, private_key=private_key, passphrase=passphrase)


def create_ps384_algorithm(public_key, private_key, passphrase=None):
    return RsaAlgorithm('PS384', public_key=public_key, private_key=private_key, passphrase=passphrase)


def create_ps512_algorithm(public_key, private_key, passphrase=None):
    return RsaAlgorithm('PS512', public_key=public_key, private_key=private_key, passphrase=passphrase)


def create_es256_algorithm(public_key, private_key, passphrase=None):
    return EcdsaAlgorithm('ES256', public_key=public_key, private_key=private_key, passphrase=passphrase)


def create_es256k_algorithm(public_key, private_key, passphrase=None):
    return EcdsaAlgorithm('ES256K', public_key=public_key, private_key=private_key, passphrase=passphrase)


def create_es384_algorithm(public_key, private_key, passphrase=None):
    return EcdsaAlgorithm('ES384', public_key=public_key, private_key=private_key, passphrase=passphrase)


def create_es521_algorithm(public_key, private_key, passphrase=None):
    return EcdsaAlgorithm('ES521', public_key=public_key, private_key=private_key, passphrase=passphrase)


def create_es512_algorithm(public_key, private_key, passphrase=None):
    return EcdsaAlgorithm('ES512', public_key=public_key, private_key=private_key, passphrase=passphrase)
