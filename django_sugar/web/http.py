r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import logging
import re
from typing import List

from django.utils import deprecation
from rest_framework.response import Response


def merge_client_data(request, *, squeeze=True, default_values: dict = None, **kwargs):
    """
    合并请求提交的数据

    :param request: 请求对象
    :param squeeze: 当结果value包含多个值时，是否只去最后一个值
    :param default_values: 可以设置一些缺省值
    :param kwargs: 其他参数
    :return: 合并后的数据(字典)
    """
    default_values = default_values or dict()

    ret = {
        **default_values,
        **kwargs,
        **request.GET,
        **request.data,
    }

    if squeeze:
        for k, v in ret.items():
            if isinstance(v, List):
                v = list[-1]
                ret.update({k: v})

    return ret


def bind_request_data(request, serializer_class, *, squeeze=True, default_values: dict = None, **kwargs):
    """
    绑定请求数据

    :param request: 请求对象
    :param serializer_class: 序列化器类型
    :param squeeze: 当结果value包含多个值时，是否只去最后一个值
    :param default_values: 可以设置一些缺省值
    :param kwargs: 其他参数
    :return: 合并后的数据(字典)
    """

    data = merge_client_data(request, squeeze=squeeze, default_values=default_values, **kwargs)
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def serialize_data_to_response(data, serializer_class=None, *, many=False, **kwargs):
    """
    序列化数据到response对象

    :param data: 待序列化的数据
    :param serializer_class: 序列化器类型
    :param many: 是否序列化多个元素
    :return: Response实例
    """

    if serializer_class:
        serializer = serializer_class(instance=data, many=many, **kwargs)
        data = serializer.data
    return Response(data=data)


def maybe_spider(request):
    """
    测试请求是否有可能是有蜘蛛/爬虫发起

    本函数参数仅作为参考

    :param request: 请求对象
    :return: 有可能是爬虫时返回True
    """
    user_agent = request.headers.get('User-Agent', None)
    if not user_agent:
        return False

    regex = r"qihoobot|Baiduspider|Googlebot|Googlebot-Mobile|Googlebot-Image|Mediapartners-Google|" \
            r"Adsbot-Google|Feedfetcher-Google|Yahoo! Slurp|Yahoo! Slurp China|YoudaoBot|Sosospider|" \
            r"Sogou spider|Sogou web spider|MSNBot|ia_archiver|Tomato Bot"
    return bool(re.search(regex, user_agent))


class HttpRequestDescriptor(object):
    """
    http请求描述器

    本质上这是一个HttpRequest的装饰器
    """

    def __init__(self, request):
        """
        构造方法
        :param request: 请求对象
        """
        self._request = request

    def get_base_info(self):
        return {
            'schema': self._request.scheme,
            'is_secure': self._request.is_secure(),
            'method': self._request.method,
            'path': self._request.path,
        }

    def get_headers(self):
        return {
            **self._request.headers,
        }

    def get_query_params(self):
        return {
            **self._request.GET,
        }

    @property
    def native_request(self):
        return self._request

    def get_detail(self):
        ret = list()

        # 基本信息
        ret.append("Base Information:")
        for name, content in self.get_base_info().items():
            ret.append("\t%s => %s" % (name, content))

        # 元信息
        ret.append("Meta:")
        for name, content in self._request.META.items():
            if name.startswith('HTTP_') or name in ['REMOTE_ADDR']:
                ret.append("\t%s => %s" % (name, content))

        # 请求头
        if len(self.get_headers()) > 0:
            ret.append("Headers:")
            for name, value in self.get_headers().items():
                ret.append("\t%s => %s" % (name, value))

        # query参数
        if len(self.get_query_params()):
            ret.append("Query Dict:")
            for k, v in self.get_query_params().items():
                ret.append("\t%s => %s" % (k, v))

        return ret

    def __str__(self):
        return '\n'.join(self.get_detail())

    def __repr__(self):
        return str(self)


# ----------------------------------------------------------------------------------------------------------------------


class RequestLoggingMiddleware(deprecation.MiddlewareMixin):
    """
    请求日志记录中间件
    """

    def process_request(self, request):
        descriptor = HttpRequestDescriptor(request)
        logging.debug('-' * 120)
        for msg in descriptor.get_detail():
            logging.debug(msg)
        logging.debug('-' * 120)
        return self.get_response(request)
