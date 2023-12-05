"""..."""
from dataclasses import dataclass

from common.libs.alidrive.types import DatClass


@dataclass
class GetDefaultDriveRequest(DatClass):
    """..."""
    user_id: str
