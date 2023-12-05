"""GetFilePathResponse"""
from dataclasses import dataclass, field
from typing import List

from common.libs.alidrive import DatClass, BaseFile


@dataclass
class GetFilePathResponse(DatClass):
    """GetFilePathResponse"""
    items: List[BaseFile] = field(default_factory=list)
