"""..."""

from .Create import Create
from .Download import Download
from .Drive import Drive
from .User import User
from .File import File
from .Recyclebin import Recyclebin


class Core(
    Create,
    Download,
    Drive,
    User,
    File,
    Recyclebin
):
    """..."""
