r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
import string

from rest_framework import fields


class PasswordField(fields.CharField):
    """
    密码(口令)相关Field

    用于序列化器
    """
    default_error_messages = {
        'invalid': "Invalid password.",
    }

    must_contains_lower_case_letter = True
    must_contains_upper_case_letter = True
    must_contains_special_character_letter = True
    special_character_set = None

    def __init__(self, *,
                 must_contains_lower_case_letter=True,
                 must_contains_upper_case_letter=True,
                 must_contains_special_character_letter=True,
                 special_character_set=None,
                 **kwargs):
        self.must_contains_lower_case_letter = must_contains_lower_case_letter
        self.must_contains_upper_case_letter = must_contains_upper_case_letter
        self.must_contains_special_character_letter = must_contains_special_character_letter
        self.special_character_set = special_character_set or r'!@#$%^&*()_+-,./<>/?;:|'
        super().__init__(**kwargs)

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        # 检查特殊字符包含情况
        ng1 = True
        if self.must_contains_special_character_letter:
            for ch in ret:
                if ch in self.special_character_set:
                    ng1 = False
                    break
        else:
            ng1 = False

        # 检查小写字符包含情况
        ng2 = True
        if self.must_contains_lower_case_letter:
            for ch in ret:
                if ch in string.ascii_lowercase:
                    ng2 = False
                    break
        else:
            ng2 = False

        # 检查大写字符包含情况
        ng3 = True
        if self.must_contains_upper_case_letter:
            for ch in ret:
                if ch in string.ascii_uppercase:
                    ng3 = False
                    break
        else:
            ng3 = False

        if ng1 or ng2 or ng3:
            self.fail('invalid')

        return ret
