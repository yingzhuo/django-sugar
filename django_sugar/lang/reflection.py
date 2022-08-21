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

class ReflectionComponentMixin(object):
    """
    反射特质
    """

    def get_attribute(self, attr_name, raise_error=False):
        attr = self.__getattribute__(attr_name)
        if attr is not None:
            return attr

        if raise_error:
            msg = "%s attribute not found" % (attr_name,)
            raise TypeError(msg)
        else:
            return None

    def get_callable(self, attr_name, raise_error=False):
        attr = self.get_attribute(attr_name, raise_error)

        if not callable(attr):
            attr = None

        if attr is not None:
            return attr

        if raise_error:
            msg = "%s callable attribute not found" % (attr_name,)
            raise TypeError(msg)
        else:
            return None
