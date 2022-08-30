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
from typing import Optional, Dict, Any

import jwt
from jwt import exceptions

from django_sugar.lang import reflection
from django_sugar.web import token


class JWTTokenParser(token.BearerTokenResolver):
    """
    JWT令牌解析器
    """

    def resolve_token(self, request, **kwargs):
        tk = super().resolve_token(request, **kwargs)

        # 检查令牌中包含两个点号
        # 否则不可能是JWT格式令牌
        dot_count = 0
        for ch in tk:
            if ch == '.':
                dot_count += 1

        if dot_count != 2:
            return None

        return tk


# ----------------------------------------------------------------------------------------------------------------------

class JWTException(Exception):
    """
    JWT相关所有的异常的基础类
    """
    pass


class DecodeException(JWTException):
    """
    令牌解析不成功
    """
    pass


class InvalidSignatureException(JWTException):
    """
    非法的签名
    """
    pass


class ExpiredSignatureException(JWTException):
    """
    令牌已过期
    """
    pass


class InvalidAudienceException(JWTException):
    """
    非法的Audience信息
    """
    pass


class InvalidIssuerException(JWTException):
    """
    非法的Issuer信息
    """
    pass


class InvalidIssuedAtException(JWTException):
    """
    非法的IssuerAt信息
    """
    pass


class ImmatureSignatureException(JWTException):
    """
    不完整的签名
    """
    pass


class InvalidAlgorithmException(JWTException):
    """
    非法的算法
    """
    pass


class MissingRequiredClaimException(JWTException):
    """
    缺失关键Claim
    """
    pass


# ----------------------------------------------------------------------------------------------------------------------


class JWTTokenBasedUserFinder(token.TokenBasedUserFinder, metaclass=abc.ABCMeta):
    def map_exception(self, ex):

        if isinstance(ex, exceptions.ExpiredSignatureError):
            return ExpiredSignatureException(str(ex))

        if isinstance(ex, exceptions.InvalidSignatureError):
            return InvalidSignatureException(str(ex))

        if isinstance(ex, exceptions.InvalidAudienceError):
            return InvalidAudienceException(str(ex))

        if isinstance(ex, exceptions.InvalidIssuerError):
            return InvalidIssuerException(str(ex))

        if isinstance(ex, exceptions.InvalidIssuedAtError):
            return InvalidIssuedAtException(str(ex))

        if isinstance(ex, exceptions.ImmatureSignatureError):
            return ImmatureSignatureException(str(ex))

        if isinstance(ex, exceptions.InvalidAlgorithmError):
            return InvalidAlgorithmException(str(ex))

        if isinstance(ex, exceptions.MissingRequiredClaimError):
            return MissingRequiredClaimException(str(ex))

        if isinstance(ex, exceptions.PyJWTError):
            return JWTException(str(ex))

        return None


_DEFAULT_HS256_SECRET = 'django-sugar:HS256@@secret-1234567890'


class HS256JWTTokenBasedUserFinder(JWTTokenBasedUserFinder):
    """
    HS256算法JWT相关的用户信息查找器
    """

    # 加密key
    hs256_secret = _DEFAULT_HS256_SECRET

    # 是否要验证JWT的签名
    jwt_verify_signature = True

    # 是否要验证exp
    jwt_verify_exp = True

    # 是否要验证nbf
    jwt_verify_nbf = True

    # 是否要验证iat
    jwt_verify_iat = False

    # 是否要验证iss
    jwt_verify_iss = False

    # 是否要验证aud
    jwt_verify_aud = False

    # 比需要有的 claims_name 默认无要求
    jwt_required_claims_names = []

    def get_user_by_token(self, jwt_token, **kwargs):
        user_info = self._parse_token(jwt_token)

        if not user_info:
            return None

        # 尝试调用钩子方法转换类型
        convert_user = reflection.get_callable_attribute(self, 'convert_user', raise_error=False)
        if convert_user:
            return convert_user(user_info)
        else:
            return user_info

    def _parse_token(self, jwt_token) -> Optional[dict]:
        try:
            options = {
                'verify_signature': self.jwt_verify_signature,
                'verify_exp': self.jwt_verify_exp,
                'verify_nbf': self.jwt_verify_nbf,
                'verify_iss': self.jwt_verify_iss,
                'verify_iat': self.jwt_verify_iat,
                'verify_aud': self.jwt_verify_aud,
            }

            if self.jwt_required_claims_names:
                options['require'] = self.jwt_required_claims_names

            return jwt.decode(jwt_token, key=self.hs256_secret, algorithms=['HS256'], options=options)
        except exceptions.PyJWTError as exc:
            exc = self.map_exception(exc)
            if exc is None:
                return None
            else:
                raise exc


# ----------------------------------------------------------------------------------------------------------------------


class HS256JWTTokenGenerator(token.TokenGenerator, metaclass=abc.ABCMeta):
    """
    JWT令牌生成器

    此类为抽象类。
    """

    # 加密key
    hs256_secret = _DEFAULT_HS256_SECRET

    def generate_token(self, user, **kwargs):
        jwt_payload = self.user_to_jwt_payload(user)
        return jwt.encode(jwt_payload, self.hs256_secret, algorithm='HS256')

    @abc.abstractmethod
    def user_to_jwt_payload(self, user) -> Optional[Dict[str, Any]]:
        """
        用户对象转换成字典类型，以便生成JWT令牌

        特殊claim键共有五个:
        “exp” (Expiration Time) Claim (UTC)
        “nbf” (Not Before Time) Claim (UTC)
        “iss” (Issuer) Claim
        “aud” (Audience) Claim
        “iat” (Issued At) Claim

        :param user: 用户对象
        :return: 字典
        """
