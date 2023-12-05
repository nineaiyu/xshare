"""..."""

from dataclasses import dataclass, field
from typing import List

from common.libs.alidrive.types import DatClass


@dataclass
class BatchMoveToTrashRequest(DatClass):
    """..."""
    file_id_list: List[str] = field(default_factory=list)
    drive_id: str = None
