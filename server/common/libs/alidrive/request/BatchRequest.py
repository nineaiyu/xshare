"""..."""
from dataclasses import dataclass, field
from typing import List

from common.libs.alidrive.types import DataClass
from .BatchSubRequest import BatchSubRequest


@dataclass
class BatchRequest(DataClass):
    """..."""
    requests: List[BatchSubRequest] = field(default_factory=list)
    resource: str = 'file'
