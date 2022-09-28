from .base import BaseService
from ..hands import *

__all__ = ['FlowerService']


class FlowerService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def cmd(self):
        print("\n- Start Flower as Task Monitor")

        if os.getuid() == 0:
            os.environ.setdefault('C_FORCE_ROOT', '1')
        cmd = [
            'celery',
            '-A', 'xshare',
            'flower',
            '-logging=info',
            '--url_prefix=/flower',
            '--auto_refresh=False',
            '--max_tasks=1000',
            '--persistent=True',
            f'-db={APPS_DIR}/flower.db',
            '--state_save_interval=600000',
            f'--address={CELERY_FLOWER_HOST}',
            f'--port={CELERY_FLOWER_PORT}',
        ]
        if self.uid:
            cmd.extend(['--uid', self.uid])
        if self.gid:
            cmd.extend(['--gid', self.gid])
        return cmd

    @property
    def cwd(self):
        return APPS_DIR
