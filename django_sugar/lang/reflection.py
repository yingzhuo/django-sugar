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
class ReflectionComponentMixin(object):
    """
    反射特质

    混入此特质的组件可以使用便利性的方法
    """

    def get_attribute(self, attr_name, *, raise_error=False, error_msg=None):
        try:
            return self.__getattribute__(attr_name)
        except AttributeError:
            if raise_error:
                msg = error_msg or ("object has no attribute '%s'" % attr_name)
                raise TypeError(msg)
            else:
                return None

    def get_callable(self, attr_name, *, raise_error=False, error_msg=None):
        attr = self.get_attribute(attr_name, raise_error=False)

        if callable(attr):
            return attr
        elif raise_error:
            msg = error_msg or ("object has no callable attribute '%s'" % attr_name)
            raise TypeError(msg)
        else:
            return None
