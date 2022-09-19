"""..."""
from dataclasses import dataclass
from typing import Dict, Union

from common.libs.alidrive.types import DataClass
from common.libs.alidrive.types.DataClass import DataType


@dataclass
class BatchSubRequest(DataClass):
    """..."""
    body: Union[DataType, Dict]
    id: str
    url: str
    headers: Dict = None
    method: str = 'POST'

    def __post_init__(self):
        self.headers = {"Content-Type": "application/json"}
        super().__post_init__()
