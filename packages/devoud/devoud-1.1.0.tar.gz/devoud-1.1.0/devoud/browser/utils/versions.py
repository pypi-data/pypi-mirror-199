import os
import json
import sys

from pkg_resources import parse_version
from urllib import request

from devoud import __version__, __name__


def version_label():
    print(f'{__name__.title()} ({__version__}) by OneEyedDancer')


def versions(package_name: str):
    url = f'https://pypi.python.org/pypi/{package_name}/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    return sorted(releases, key=parse_version, reverse=True)


def last_version(package_name: str):
    return versions(package_name)[0]


def cli_update(package_name: str):
    last = last_version(__name__)
    current = __version__
    if current == last:
        print('[Обновление]: У вас установлена последняя версия программы')
        return
    print(f'[Обновление]: Доступно {__version__} -> {last_version(__name__)}')
    if sys.platform == 'win32':
        return print('[Обновление]: Данная опция не доступна для систем Windows, используйте "pip install devoud --upgrade"')
    if input('[Обновление]: Установить обновления? [y/n]: ').lower() == 'y':
        os.system(f'pip3 install {package_name} --upgrade')
    else:
        print('Отмена операции')
