"""..."""
from dataclasses import dataclass, field
from typing import List

from common.libs.alidrive.types import DataClass, BaseDrive


@dataclass
class ListMyDrivesResponse(DataClass):
    """..."""
    items: List[BaseDrive] = field(default_factory=list)
    next_marker: str = ''
