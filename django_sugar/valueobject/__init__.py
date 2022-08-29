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
import abc

from rest_framework import serializers

from django_sugar.valueobject.color import Color, ColorField
from django_sugar.valueobject.daterange import DateRange, DateRangeField
from django_sugar.valueobject.intrange import IntRange, IntRangeField
from django_sugar.valueobject.intrangecollection import IntRangeCollection, IntRangeCollectionField


# ----------------------------------------------------------------------------------------------------------------------

class AbstractField(serializers.Field, metaclass=abc.ABCMeta):

    def to_representation(self, value):
        return str(value)
