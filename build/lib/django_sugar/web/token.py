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
import string

from django_sugar import lang


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


class QueryTokenResolver(TokenResolver):
    """
    令牌解析器具体实现

    从请求参数中获取令牌数据
    """

    token_parameter_name = '_token'

    def resolve_token(self, request, **kwargs):
        token_value = request.GET.get(self.token_parameter_name, None)
        token_value = lang.blank_to_none(token_value)
        return token_value


class HeaderTokenResolver(TokenResolver):
    """
    令牌解析器具体实现

    从请求头中获取令牌数据
    """

    # 请求头名
    header_name = 'Authorization'

    # 期望的令牌的前缀
    token_value_prefix = 'Token '

    def resolve_token(self, request, **kwargs):
        token_value = request.headers.get(self.header_name, None)
        token_value = lang.blank_to_none(token_value)

        if token_value is None or not lang.startswith(token_value, self.token_value_prefix, ignore_cases=True):
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

    def resolve_username_and_password(self, request, **kwargs):
        token = self.resolve_token(request, **kwargs)
        if token:
            uap = lang.base64_standard_decode(token).split(':', 2)
            return uap[0], uap[1]
        else:
            return None, None


class CompositeTokenResolver(TokenResolver):
    """
    复合型令牌解析器

    代理其他类型令牌解析器，并将第一个能正确解析出令牌的解析的结果返回。
    """

    token_resolver_classes = [HeaderTokenResolver, BearerTokenResolver, BasicTokenResolver, ]

    def __len__(self):
        return len(self.token_resolver_classes)

    def __iter__(self):
        for t in self.token_resolver_classes:
            yield t()

    def __getitem__(self, item):
        ret = self.token_resolver_classes[item]
        if lang.is_iterable(ret):
            return map(lambda x: x(), ret)
        else:
            return ret()

    def resolve_token(self, request, **kwargs):
        for token_resolver in self.get_token_resolvers():
            # noinspection PyBroadException
            try:
                ret = token_resolver.resolve_token(request, **kwargs)
                if ret is not None:
                    return ret
            except Exception:
                continue
        return None

    def get_token_resolvers(self):
        return [x() for x in self.token_resolver_classes]


# ----------------------------------------------------------------------------------------------------------------------

class TokenGenerator(object, metaclass=abc.ABCMeta):
    """
    令牌生成器

    本类是抽象的。
    """

    def generate_token(self, user, **kwargs):
        """
        为用户生成令牌
        :param user: 用户对象
        :param kwargs: 其他参数
        :return: 令牌字符串
        """


class RandomUUIDTokenGenerator(TokenGenerator):
    """
    令牌生成器具体实现

    生成随机UUID作为令牌
    """

    remove_uuid_hyphen = False

    def generate_token(self, user, **kwargs):
        return lang.random_uuid(remove_hyphen=self.remove_uuid_hyphen)


class MD5TokenGenerator(TokenGenerator):
    """
    令牌生成器具体实现

    使用MD5信息摘要发生成令牌
    """

    def generate_token(self, user, **kwargs):
        return lang.md5(str(user))


class SimpleRandomStringTokenGenerator(TokenGenerator):
    """
    令牌生成器具体实现

    生成简单的随机字符串
    """

    length = 36
    chars_to_choice = string.ascii_letters

    def generate_token(self, user, **kwargs):
        return lang.random_string(self.length, chars=self.chars_to_choice)


# ----------------------------------------------------------------------------------------------------------------------


class TokenBasedUserFinder(object, metaclass=abc.ABCMeta):
    """
    通过token获取用户实例的组件

    此类为抽象类。
    """

    @abc.abstractmethod
    def get_user_by_token(self, current_token, **kwargs):
        """
        从令牌中获取用户信息
        :param current_token: 当前用于发送的令牌
        :param kwargs: 其他参数
        :return: 用户信息
        """
