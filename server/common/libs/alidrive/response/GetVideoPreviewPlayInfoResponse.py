"""..."""
from dataclasses import dataclass

from common.libs.alidrive.types import DataClass, VideoPreviewPlayInfo


@dataclass
class GetVideoPreviewPlayInfoResponse(DataClass):
    """..."""
    domain_id: str = None
    drive_id: str = None
    file_id: str = None
    video_preview_play_info: VideoPreviewPlayInfo = None
