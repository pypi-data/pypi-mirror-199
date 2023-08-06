"""pycasreg."""
import importlib.metadata
from typing import Union


def _get_version_tuple() -> tuple:
    def as_integer(version_str: str) -> Union[int, str]:
        try:
            return int(version_str)
        except ValueError:  # pragma: no cover
            return version_str  # pragma: no cover

    return tuple(
        as_integer(v) for v in importlib.metadata.version("pycasreg").strip().split(".")
    )


__version__ = _get_version_tuple()
