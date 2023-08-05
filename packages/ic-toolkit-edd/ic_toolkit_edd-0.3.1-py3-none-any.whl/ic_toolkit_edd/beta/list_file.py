import os
import stat
from pathlib import Path


def is_hidden(file: Path):
    if file.name.startswith('.'):
        return True
    if has_hidden_attribute(file):
        return True


def has_hidden_attribute(file: Path):
    try:
        return os.stat(file).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN
    except:
        return False


def is_office_lock(file: Path):
    file.name.startswith('~$')


def get_files(path: str = '.'):
    for file in Path(path).iterdir():
        if file.is_file():
            if is_hidden(file):
                continue
            if is_office_lock(file):
                continue
            yield file
