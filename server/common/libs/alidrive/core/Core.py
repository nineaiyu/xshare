"""..."""

from .Create import Create
from .Download import Download
from .Drive import Drive
from .File import File
from .Recyclebin import Recyclebin
from .User import User


class Core(
    Create,
    Download,
    Drive,
    User,
    File,
    Recyclebin
):
    """..."""
