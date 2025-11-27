import os


def join(*paths: str) -> str:
    a, *p = paths
    return str(os.path.join(a, *p))


def directory_name(path: str) -> str:
    return os.path.dirname(path)


def basename(path: str) -> str:
    return os.path.basename(path)


def is_absolute(path: str) -> bool:
    return os.path.isabs(path)


def is_relative(path: str) -> bool:
    return not is_absolute(path)


def to_absolute(path: str) -> str:
    return os.path.abspath(path)


def exists(path: str) -> bool:
    return os.path.exists(path)


def exists_directory(path: str) -> bool:
    return os.path.isdir(path)


def exists_file(path: str) -> bool:
    return os.path.isfile(path)


def make_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)
