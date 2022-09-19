"""..."""
from dataclasses import dataclass

from common.libs.alidrive.types import DataClass


@dataclass
class PersonalSpaceInfo(DataClass):
    """..."""
    used_size: int = None
    total_size: int = None
