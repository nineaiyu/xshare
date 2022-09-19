"""GetFilePathResponse"""
from dataclasses import dataclass, field
from typing import List

from common.libs.alidrive import DataClass, BaseFile


@dataclass
class GetFilePathResponse(DataClass):
    """GetFilePathResponse"""
    items: List[BaseFile] = field(default_factory=list)
