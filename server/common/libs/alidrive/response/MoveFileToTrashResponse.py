"""..."""
from dataclasses import dataclass

from common.libs.alidrive.types import DataClass


@dataclass
class MoveFileToTrashResponse(DataClass):
    """..."""
    file_id: str = None
    drive_id: str = None
    domain_id: str = None
    async_task_id: str = None
