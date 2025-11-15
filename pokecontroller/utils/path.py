import os

ROOT_DIR = os.name == "nt" and "C:" or "/"


def is_absolute(path: str) -> bool:
    return os.path.isabs(path)


def is_relative(path: str) -> bool:
    return not is_absolute(path)


def to_absolute(path: str) -> str:
    return os.path.abspath(path)


def is_dir(path: str) -> bool:
    return os.path.isdir(path)


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def join(*paths: str) -> str:
    return str(os.path.join(*paths))
