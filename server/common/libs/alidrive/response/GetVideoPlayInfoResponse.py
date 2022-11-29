"""..."""
from dataclasses import dataclass
from typing import List

from common.libs.alidrive import DataClass
from common.libs.alidrive.types import VideoTranscodeTemplate


@dataclass
class GetVideoPlayInfoResponse(DataClass):
    """..."""
    template_list: List[VideoTranscodeTemplate] = None
