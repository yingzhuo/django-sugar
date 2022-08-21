#
#  ____                           ____
# |  _ \(_) __ _ _ __   __ _  ___/ ___| _   _  __ _  __ _ _ __
# | | | | |/ _` | '_ \ / _` |/ _ \___ \| | | |/ _` |/ _` | '__|
# | |_| | | (_| | | | | (_| | (_) |__) | |_| | (_| | (_| | |
# |____// |\__,_|_| |_|\__, |\___/____/ \__,_|\__, |\__,_|_|
#    |__/             |___/                  |___/
#
# https://github.com/yingzhuo/django-sugar
#
import abc

from django_sugar.lang import string_tool


class TokenResolver(object, metaclass=abc.ABCMeta):
    """
    令牌解析器

    本组件只有一个功能，即从一次Http请求中获取令牌。
    本类是抽象的。
    """

    @abc.abstractmethod
    def resolve_token(self, request, **kwargs):
        """
        从Http请求实例中获取令牌
        :param request: 请求实例
        :param kwargs: 其他可选参数
        :return: 令牌，一般是字符串类型
        """


class CompositeTokenResolver(TokenResolver):
    """
    复合型令牌解析器

    代理其他类型令牌解析器，并将第一个能正确解析出令牌的解析的结果返回。
    """

    token_resolver_classes = []

    def __init__(self, **kwargs):
        self.token_resolver_classes = kwargs.get('token_resolver_classes', [])

    def resolve_token(self, request, **kwargs):
        for token_resolver in self.get_token_resolvers():
            try:
                ret = token_resolver.resolve_token(request, kwargs)
                if ret is not None:
                    return ret
            except Exception as exc:
                continue
        return None

    def get_token_resolvers(self):
        return [x() for x in self.token_resolver_classes]


class QueryTokenResolver(TokenResolver):
    """
    令牌解析器具体实现

    从请求参数中获取令牌数据
    """

    token_parameter_name = '_token'

    def resolve_token(self, request, **kwargs):
        token_value = request.GET.get(self.token_parameter_name, None)
        token_value = string_tool.blank_to_none(token_value)
        return token_value


class HeaderTokenResolver(TokenResolver):
    """
    令牌解析器具体实现

    从请求头中获取令牌数据
    """

    # 请求头名
    header_name = 'X-Token'

    # 期望的令牌的前缀
    token_value_prefix = ''

    def resolve_token(self, request, **kwargs):
        token_value = request.headers.get(self.header_name, None)
        token_value = string_tool.blank_to_none(token_value)

        if token_value is None or not token_value.startswith(self.token_value_prefix):
            # 找不到此请求头或者值不以指定的前缀开始
            return None
        else:
            return token_value[len(self.token_value_prefix):]


class BearerTokenResolver(HeaderTokenResolver):
    """
    令牌解析器具体实现

    用于解析BearerToken
    """

    header_name = 'Authorization'
    token_value_prefix = 'Bearer '


class BasicTokenResolver(HeaderTokenResolver):
    """
    令牌解析器具体实现

    用于解析BasicToken
    """

    header_name = 'Authorization'
    token_value_prefix = 'Basic '
