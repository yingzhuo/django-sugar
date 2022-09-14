r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
from jwt import unregister_algorithm, register_algorithm, algorithms

from .auth import *
from .file_storage import *
from .http import *
from .jwt_base import *
from .pwd_encoder import *
from .token import *
from .token_jwt import *


# ----------------------------------------------------------------------------------------------------------------------
# 调整JWT的none算法, 疑似是bug
# https://github.com/jpadilla/pyjwt/issues/795
# ----------------------------------------------------------------------------------------------------------------------

class MyNoneAlg(algorithms.NoneAlgorithm):
    def verify(self, msg, key, sig):
        return True

    @staticmethod
    def to_jwk(key_obj):
        pass

    @staticmethod
    def from_jwk(jwk):
        pass


unregister_algorithm('none')
register_algorithm('none', MyNoneAlg())
