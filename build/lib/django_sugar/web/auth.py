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

from rest_framework import authentication

from django_sugar import lang


class Authenticator(authentication.BaseAuthentication, metaclass=abc.ABCMeta):
    """
    认证器

    本类型为抽象类。
    """

    @abc.abstractmethod
    def authenticate(self, request):
        """
        认证一个请求
        :param request: 请求实例
        :return: 认证成功时返回二元组(User, Token) 否则返回None
        """

    def authenticate_header(self, request):
        return '403 Permission Denied' if request.user else '401 Unauthenticated'


class TokenBasedAuthenticator(Authenticator):
    """
    基于令牌的认证器
    """

    # 解析令牌时发生异常是否抛出
    raise_if_token_resolving_error = True

    # 从令牌中找到用户实体时发生异常是否抛出
    raise_if_user_finding_error = True

    def authenticate(self, request):

        resolve_token = lang.get_callable_attr(self,
                                               'resolve_token',
                                               raise_error=True,
                                               error_msg='Forgot TokenResolver mixin?')

        # noinspection PyBroadException
        try:
            token = resolve_token(request)
        except Exception:
            if self.raise_if_token_resolving_error:
                raise
            else:
                token = None

        if not token:
            return None

        get_user_by_token = lang.get_callable_attr(self,
                                                   'get_user_by_token',
                                                   raise_error=True,
                                                   error_msg='Forgot TokenBasedUserFinder mixin?')

        # noinspection PyBroadException
        try:
            user = get_user_by_token(token)
        except Exception:
            if self.raise_if_user_finding_error:
                raise
            else:
                user = None

        if user:
            return user, token
        else:
            return None
