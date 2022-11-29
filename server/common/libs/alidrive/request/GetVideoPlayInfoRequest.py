"""..."""
from dataclasses import dataclass

from common.libs.alidrive import DataClass


@dataclass
class GetVideoPlayInfoRequest(DataClass):
    """..."""
    file_id: str
    drive_id: str = None
