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

def get_client_sent_data(request, *, data_over_get=True, default_values=None):
    """
    合并请求提交的数据

    :param request: 请求对象
    :param data_over_get: 为True时请求体中的数据覆盖query-params
    :param default_values: 可以设置一些缺省值
    :return: 合并后的数据(字典)
    """
    default_values = default_values or dict()

    if data_over_get:
        return {
            **default_values,
            **request.GET,
            **request.data,
        }
    else:
        return {
            **default_values,
            **request.data,
            **request.GET,
        }


# ----------------------------------------------------------------------------------------------------------------------

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
        self.request = request

    def get_base_info(self):
        return {
            'schema': self.request.scheme,
            'is_secure': self.request.is_secure(),
            'method': self.request.method,
            'path': self.request.path,
        }

    def get_headers(self):
        return {
            **self.request.headers,
        }

    def get_query_params(self):
        return {
            **self.request.GET
        }

    def get_detail(self):
        d = list()

        # 请求具体类型
        d.append("Request Type:")
        d.append("\t%s" % type(self.__class__.__qualname__))

        # 基本信息
        d.append("Base Information:")
        for name, content in self.get_base_info().items():
            d.append("\t%s => %s" % (name, content))

        # 元信息
        d.append("Meta:")
        for name, content in self.request.META.items():
            if name.startswith('HTTP_') or name in ['REMOTE_ADDR']:
                d.append("\t%s => %s" % (name, content))

        # 请求头
        if len(self.get_headers()) > 0:
            d.append("Headers:")
            for name, value in self.get_headers().items():
                d.append("\t%s => %s" % (name, value))

        # query参数
        if len(self.get_query_params()):
            d.append("Query Dict:")
            for k, v in self.get_query_params().items():
                d.append("\t%s => %s" % (k, v))

        return d

    def __str__(self):
        return '\n'.join(self.get_detail())

    def __repr__(self):
        return str(self)

# ----------------------------------------------------------------------------------------------------------------------
