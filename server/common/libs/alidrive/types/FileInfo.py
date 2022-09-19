"""..."""
from dataclasses import dataclass, field

from .DataClass import DataClass


@dataclass
class FileInfo(DataClass):
    """..."""
    sid: str = None
    file_name: str = None
    file_size: int = field(default=None, repr=False)
    pre_hash: str = field(default=None, repr=False)
    content_hash: str = field(default=None, repr=False)
    proof_code: str = field(default=None, repr=False)
