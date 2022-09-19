"""..."""
from dataclasses import dataclass

from common.libs.alidrive.types import DataClass


@dataclass
class GetDriveRequest(DataClass):
    """..."""
    drive_id: str = None
