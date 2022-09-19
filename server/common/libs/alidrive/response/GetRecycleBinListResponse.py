"""..."""
from dataclasses import dataclass, field
from typing import List

from common.libs.alidrive.types import BaseFile
from common.libs.alidrive.types import DataClass


@dataclass
class GetRecycleBinListResponse(DataClass):
    """..."""
    items: List[BaseFile] = field(default_factory=list)
    next_marker: str = ''
    punished_file_count: int = 0
