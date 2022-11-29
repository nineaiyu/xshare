"""..."""
# 导包基本原则
# 1. 包内相对导入: from .DataClass import DataClass
# 2. 包外包导入: from aligo.dataobj import xxx
from dataclasses import dataclass, field
from typing import List

from .DataClass import DataClass
from .Enum import VideoTemplateID


@dataclass
class LiveTranscodingMeta(DataClass):
    """..."""
    ts_segment: int = None
    ts_total_count: int = None
    ts_pre_count: int = None


@dataclass
class Meta(DataClass):
    """..."""
    duration: float = None
    width: int = None
    height: int = None
    live_transcoding_meta: LiveTranscodingMeta = None


@dataclass
class LiveTranscodingTask(DataClass):
    """..."""
    template_id: VideoTemplateID = None
    template_height: str = None
    template_width: str = None
    template_name: str = None
    status: str = None
    stage: str = None
    url: str = None


@dataclass
class VideoPreviewPlayInfo(DataClass):
    """..."""
    category: str = None
    meta: Meta = None
    live_transcoding_task_list: List[LiveTranscodingTask] = field(default_factory=list)
