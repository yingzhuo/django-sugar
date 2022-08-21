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

from django_sugar.lang import reflection


class Authenticator(object, metaclass=abc.ABCMeta):
    """
    认证器
    """

    @abc.abstractmethod
    def authenticate(self, request):
        """
        认证一个请求
        :param request: 请求实例
        :return:
        """

    def authenticate_header(self, request):
        return '403 Permission Denied' if request.user else '401 Unauthenticated'


class TokenBasedAuthenticator(Authenticator, reflection.ReflectionComponentMixin):

    def authenticate(self, request):

        resolve_token = self.get_callable('resolve_token',
                                          raise_error=True,
                                          error_msg='forgot TokenResolver mixin?')

        try:
            token = resolve_token(request)
        except Exception:
            token = None

        if not token:
            return None

        get_user_by_token = self.get_callable('get_user_by_token',
                                              raise_error=True,
                                              error_msg='forgot TokenBasedUserFinder mixin?')

        try:
            user = get_user_by_token(token)
        except Exception:
            user = None

        if user:
            return user, token
        else:
            return None
