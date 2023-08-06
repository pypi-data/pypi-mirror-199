import os
from typing import Callable

from .concatenate import concatenate
from .env import env

Merger = Callable[[bytes, bytes], bytes]


def get(source_name: str, dest_name: str) -> Merger:
    """
    Return the correct file merger
    """

    source_type = os.path.splitext(source_name)[1]
    dest_type = os.path.splitext(dest_name)[1]

    if source_type == ".env" and dest_type == ".env":
        return env
    else:
        return concatenate
