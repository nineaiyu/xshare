"""..."""
from dataclasses import dataclass

from common.libs.alidrive.types import DatClass


@dataclass
class GetDriveRequest(DatClass):
    """..."""
    drive_id: str = None
