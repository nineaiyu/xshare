"""..."""

from dataclasses import dataclass

from .Type import DatClass
from .Enum import MediaTranscodeStatus


@dataclass
class MediaTransCodeTemplate(DatClass):
    """..."""
    template_id: str = None
    status: MediaTranscodeStatus = None
    url: str = None
