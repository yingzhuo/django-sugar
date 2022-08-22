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
