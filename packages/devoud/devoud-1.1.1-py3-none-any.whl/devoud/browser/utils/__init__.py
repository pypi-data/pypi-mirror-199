import os
from pathlib import Path
from subprocess import Popen
from sys import platform


def human_bytes(B):
    """Возвращает байты в нормальном виде (B, KB, MB, GB, TB)"""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)


def open_in_file_manager(path):
    path = Path(path)
    """Открывает путь через системный файловый менеджер"""
    command = {'win32': ["explorer", path],
               'darwin': ["open", path],
               'linux': ["xdg-open", path]}
    Popen(command.get(platform, ["xdg-open", path]))


def get_folder_size(path) -> int:
    size = 0
    for path, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            try:
                size += os.path.getsize(fp)
            except FileNotFoundError:
                pass
    return size
