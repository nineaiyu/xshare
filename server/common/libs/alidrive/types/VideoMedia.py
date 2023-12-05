"""..."""
from dataclasses import dataclass
from typing import List

from .Type import DatClass
from .ImageTag import ImageTag
from .VideoMediaAudioStream import VideoMediaAudioStream
from .VideoMediaVideoStream import VideoMediaVideoStream


@dataclass
class VideoMedia(DatClass):
    """..."""
    time: str = None
    city: str = None
    country: str = None
    address_line: str = None
    district: str = None
    duration: str = None
    height: int = None
    location: str = None
    province: str = None
    township: str = None
    video_media_audio_stream: List[VideoMediaAudioStream] = None
    video_media_video_stream: List[VideoMediaVideoStream] = None
    width: int = None
    image_tags: List[ImageTag] = None
