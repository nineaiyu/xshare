from .base import BaseService
from ..hands import *

__all__ = ['GunicornService']


class GunicornService(BaseService):

    def __init__(self, **kwargs):
        self.worker = kwargs['worker_gunicorn']
        super().__init__(**kwargs)

    @property
    def cmd(self):
        print("\n- Start Gunicorn WSGI HTTP Server")

        log_format = '%(h)s %(t)s %(L)ss "%(r)s" %(s)s %(b)s '
        bind = f'{HTTP_HOST}:{HTTP_PORT}'
        cmd = [
            'gunicorn', 'xshare.wsgi',
            '-b', bind,
            '-k', 'gthread',
            '--threads', '10',
            '-w', str(self.worker),
            '--max-requests', '4096',
            '--access-logformat', log_format,
            '--access-logfile', '-'
        ]
        if self.uid:
            cmd.extend(['--user', self.uid])
        if self.gid:
            cmd.extend(['--group', self.gid])
        if DEBUG:
            cmd.append('--reload')
        return cmd

    @property
    def cwd(self):
        return APPS_DIR
