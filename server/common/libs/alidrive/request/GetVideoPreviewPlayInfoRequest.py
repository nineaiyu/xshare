"""..."""
from dataclasses import dataclass

from common.libs.alidrive.types import DatClass
from common.libs.alidrive.types.Enum import GetVideoPreviewCategory, VideoTemplateID


@dataclass
class GetVideoPreviewPlayInfoRequest(DatClass):
    """..."""
    file_id: str = None
    drive_id: str = None
    category: GetVideoPreviewCategory = 'live_transcoding'
    template_id: VideoTemplateID = None
    url_expire_sec: int = 14400
