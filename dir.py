import os
def get_base_dir() -> str:
    return get_dir(__file__)


def get_dir(mod: str) -> str:
    return os.path.abspath(os.path.dirname(os.path.abspath(mod)))