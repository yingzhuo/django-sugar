r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
from django.db import connection


def raw_query(sql: str, *, params=None, many=True):
    """
    原生SQL查询数据

    :param sql: 语句
    :param params: sql参数
    :param many: 查询多个结果集时为True，否者为False
    :return: 查询结果
    """
    if many:
        return _raw_query_many(sql, params=params)
    else:
        return _raw_query_single(sql, params=params)


def _raw_query_many(sql: str, *, params=None):
    with connection.cursor() as cursor:
        if params:
            cursor.execute(sql, params=params)
        else:
            cursor.execute(sql)

        column_names = [it[0] for it in cursor.description]
        rows = cursor.fetchall()
        result = []
        for row in rows:
            data = dict(zip(column_names, row))
            result.append(data)
        return result


def _raw_query_single(sql: str, *, params=None):
    with connection.cursor() as cursor:
        if params:
            cursor.execute(sql, params=params)
        else:
            cursor.execute(sql)
        col_names = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        if row and col_names:
            return dict(zip(col_names, row))
        else:
            return None
