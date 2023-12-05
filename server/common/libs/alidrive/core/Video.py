"""..."""

from common.libs.alidrive.core import *
from common.libs.alidrive.core.Config import *
from common.libs.alidrive.request import *
from common.libs.alidrive.response import *


class Video(BaseAligo):
    """..."""

    def _core_get_video_play_info(self, body: GetVideoPlayInfoRequest) -> GetVideoPlayInfoResponse:
        """..."""
        response = self._post(V2_DATABOX_GET_VIDEO_PLAY_INFO, body=body)
        return self._result(response, GetVideoPlayInfoResponse)

    def _core_get_video_preview_play_info(
            self,
            body: GetVideoPreviewPlayInfoRequest
    ) -> GetVideoPreviewPlayInfoResponse:
        """可获取m3u8链接"""
        response = self._post(V2_FILE_GET_VIDEO_PREVIEW_PLAY_INFO, body=body)
        return self._result(response, GetVideoPreviewPlayInfoResponse)

