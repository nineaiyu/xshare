"""..."""
from dataclasses import dataclass
from typing import List

from common.libs.alidrive import DatClass
from common.libs.alidrive.types import VideoTranscodeTemplate


@dataclass
class GetVideoPlayInfoResponse(DatClass):
    """..."""
    template_list: List[VideoTranscodeTemplate] = None
