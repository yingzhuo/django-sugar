r"""
 ____  _                           ____
|  _ \(_) __ _ _ __   __ _  ___   / ___| _   _  __ _  __ _ _ __
| | | | |/ _` | '_ \ / _` |/ _ \  \___ \| | | |/ _` |/ _` | '__|
| |_| | | (_| | | | | (_| | (_) |  ___) | |_| | (_| | (_| | |
|____// |\__,_|_| |_|\__, |\___/  |____/ \__,_|\__, |\__,_|_|
    |__/             |___/                     |___/

    https://github.com/yingzhuo/django-sugar

"""
from setuptools import setup, find_packages

import django_sugar as sugar

setup(
    name='django_sugar',
    version=sugar.VERSION,
    author='应卓',
    author_email='yingzhor@gmail.com',
    url=r'https://github.com/yingzhuo/django-sugar',
    packages=find_packages(),
    install_requires=[
        'django>=4.1.1',
        'djangorestframework>=3.13.1',
        'PyJWT>=2.4.0',
        'cryptography>=38.0.1',
    ],
)
