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


class JsonWebTokenSignatureComponent(object, metaclass=abc.ABCMeta):
    """
    JWT签名算法组件

    本组件包含算法和签名key

    提示:

    生成密钥文件 (ECDSA):
    openssl ecparam -name prime256v1 -genkey -noout -out ecdsa_private.key
    openssl ec -in ecdsa_private.key -pubout -out ecdsa_public.key

    生成密钥文件 (RSA without passphrase):
    openssl genrsa -out rsa_private.key 2048
    openssl rsa -in rsa_private.key -pubout -out rsa_public.key

    生成密钥文件 (RSA with passphrase)
    openssl genrsa -aes256 -passout pass:<passphrase> -out rsa_private.key 2048
    openssl rsa -in rsa_private.key -passin pass:<passphrase> -pubout -out rsa_public.key
    """

    @abc.abstractmethod
    def name(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def encoding_key(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def decoding_key(self):
        raise NotImplementedError()

    @staticmethod
    def none():
        return _NONE()

    @staticmethod
    def hs256(key):
        return _HMAC('HS256', key)

    @staticmethod
    def hs384(key):
        return _HMAC('HS384', key)

    @staticmethod
    def hs512(key):
        return _HMAC('HS512', key)

    @staticmethod
    def rs256(public_key, private_key, passphrase=None):
        return _RSA('RS256', public_key, private_key, passphrase)

    @staticmethod
    def rs384(public_key, private_key, passphrase=None):
        return _RSA('RS384', public_key, private_key, passphrase)

    @staticmethod
    def rs512(public_key, private_key, passphrase=None):
        return _RSA('RS512', public_key, private_key, passphrase)

    @staticmethod
    def ps256(public_key, private_key, passphrase=None):
        return _RSA('PS256', public_key, private_key, passphrase)

    @staticmethod
    def ps384(public_key, private_key, passphrase=None):
        return _RSA('PS384', public_key, private_key, passphrase)

    @staticmethod
    def ps512(public_key, private_key, passphrase=None):
        return _RSA('PS512', public_key, private_key, passphrase)

    @staticmethod
    def es256(public_key, private_key):
        return _ECDSA('ES256', public_key, private_key)

    @staticmethod
    def es256k(public_key, private_key):
        return _ECDSA('ES256K', public_key, private_key)

    @staticmethod
    def es384(public_key, private_key):
        return _ECDSA('ES384', public_key, private_key)

    @staticmethod
    def es521(public_key, private_key):
        return _ECDSA('ES521', public_key, private_key)

    @staticmethod
    def es512(public_key, private_key):
        return _ECDSA('ES512', public_key, private_key)


class _NONE(JsonWebTokenSignatureComponent):

    @property
    def name(self):
        return 'none'

    @property
    def encoding_key(self):
        return None

    @property
    def decoding_key(self):
        return None


class _HMAC(JsonWebTokenSignatureComponent):

    def __init__(self, name, key):
        self._name = name
        self._key = lang.ensure_string(key)
        pass

    @property
    def name(self):
        return self._name

    @property
    def encoding_key(self):
        return self._key

    @property
    def decoding_key(self):
        return self._key


class _RSA(JsonWebTokenSignatureComponent):

    def __init__(self, name, public_key, private_key, passphrase=None):
        public_key = lang.ensure_bytes(public_key)
        private_key = lang.ensure_bytes(private_key)
        passphrase = lang.ensure_bytes(passphrase)

        if passphrase is not None:
            private_key = serialization.load_pem_private_key(private_key,
                                                             password=passphrase,
                                                             backend=default_backend())
        self._name = name
        self._public_key = public_key
        self._private_key = private_key

    @property
    def name(self):
        return self._name

    @property
    def encoding_key(self):
        return self._private_key

    @property
    def decoding_key(self):
        return self._public_key


class _ECDSA(JsonWebTokenSignatureComponent):

    def __init__(self, name, public_key, private_key):
        public_key = lang.ensure_bytes(public_key)
        private_key = lang.ensure_bytes(private_key)

        self._name = name
        self._public_key = public_key
        self._private_key = private_key

    @property
    def name(self):
        return self._name

    @property
    def encoding_key(self):
        return self._private_key

    @property
    def decoding_key(self):
        return self._public_key
