r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import datetime
import typing

from django.core import exceptions
from django.core.files import storage
from django.utils import timezone


class FileSavePolicy(object):
    """
    文件保存策略
    """

    def __init__(self, *,
                 prefix_application='',
                 prefix_timestamp_format='%Y-%m-%d',
                 suffix=None,
                 ):
        self._prefix_timestamp_format = prefix_timestamp_format
        self._prefix_application = prefix_application
        self._suffix = suffix

    def get_filename_prefix(self):
        ret = ''

        if self._prefix_application:
            ret += self._prefix_application + '/'

        if self._prefix_timestamp_format is not None:
            try:
                ret += timezone.now().strftime(self._prefix_timestamp_format) + '/'
            except exceptions.ImproperlyConfigured:
                ret += datetime.datetime.now().strftime(self._prefix_timestamp_format) + '/'

        return ret

    def get_filename_suffix(self):
        if isinstance(self._suffix, str):
            return self._suffix
        elif isinstance(self._suffix, typing.Callable):
            return str(self._suffix())
        else:
            return ''


class SmartFileSystemFileStorage(storage.FileSystemStorage):
    """
    智能本地文件保存器
    """

    def __init__(self, file_save_policy=None, **kwargs):
        self.file_save_policy = file_save_policy or FileSavePolicy()
        super().__init__(**kwargs)

    def save(self, name, content, max_length=None):
        if isinstance(name, (str,)):
            name = self.file_save_policy.get_filename_prefix() + name
            name = name + self.file_save_policy.get_filename_suffix()

        return super().save(name, content, max_length)
