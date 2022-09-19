"""..."""
from dataclasses import dataclass

from common.libs.alidrive.types import DataClass


@dataclass
class GetDefaultDriveRequest(DataClass):
    """..."""
    user_id: str
