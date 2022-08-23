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
from setuptools import setup, find_packages

import django_sugar

setup(
    name='django_sugar',
    version=django_sugar.VERSION,
    author='应卓',
    author_email='yingzhor@gmail.com',
    url=r'https://github.com/yingzhuo/django-sugar',
    packages=find_packages(),
    requires=[
    ],
)
