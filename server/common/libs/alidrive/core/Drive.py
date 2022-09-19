"""..."""

from typing import List

from common.libs.alidrive import BaseDrive
from common.libs.alidrive.core.BaseAligo import BaseAligo
from common.libs.alidrive.core.Config import *
from common.libs.alidrive.request import *
from common.libs.alidrive.response import *


class Drive(BaseAligo):
    """..."""

    def _core_get_drive(self, body: GetDriveRequest) -> BaseDrive:
        """..."""
        response = self._post(V2_DRIVE_GET, body=body)
        return self._result(response, BaseDrive)

    def get_default_drive(self) -> BaseDrive:
        """
        Get default drive.
        :return: [BaseDrive]

        :Example:
        >>> from common.libs.alidrive import Aligo
        >>> ali = Aligo()
        >>> drive = ali.get_default_drive()
        >>> print(drive.drive_name)
        """
        if self._default_drive is None:
            response = self._post(V2_DRIVE_GET_DEFAULT_DRIVE, body=GetDefaultDriveRequest(self._auth.token.user_id))
            self._default_drive = self._result(response, BaseDrive)
        return self._default_drive

    def list_my_drives(self) -> List[BaseDrive]:
        """
        List my drives.
        :return: [BaseDrive]

        :Example:
        >>> from common.libs.alidrive import Aligo
        >>> ali = Aligo()
        >>> drives = ali.list_my_drives()
        >>> for drive in drives:
        >>>     print(drive.drive_name)
        """
        # noinspection PyTypeChecker
        return list(self._list_file(V2_DRIVE_LIST_MY_DRIVES, {}, ListMyDrivesResponse))
