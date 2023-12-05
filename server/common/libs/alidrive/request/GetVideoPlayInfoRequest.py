"""..."""
from dataclasses import dataclass

from common.libs.alidrive import DatClass


@dataclass
class GetVideoPlayInfoRequest(DatClass):
    """..."""
    file_id: str
    drive_id: str = None
