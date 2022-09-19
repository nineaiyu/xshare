"""..."""
from typing import Iterator

from common.libs.alidrive.core import *
from common.libs.alidrive.core.Config import *
from common.libs.alidrive.request import *
from common.libs.alidrive.response import *
from common.libs.alidrive.types import *


class File(BaseAligo):
    """..."""

    def _core_get_file_list(self, body: GetFileListRequest) -> Iterator[BaseFile]:
        """..."""
        yield from self._list_file(ADRIVE_V3_FILE_LIST, body, GetFileListResponse)

    def _core_batch_get_files(self, body: BatchGetFileRequest) -> Iterator[BatchSubResponse]:
        """batch_get_files"""
        if body.drive_id is None:
            body.drive_id = self.default_drive_id

        yield from self.batch_request(BatchRequest(
            requests=[BatchSubRequest(
                id=file_id,
                url='/file/get',
                body=GetFileRequest(
                    drive_id=body.drive_id, file_id=file_id
                )
            ) for file_id in body.file_id_list]
        ), GetFileRequest)
