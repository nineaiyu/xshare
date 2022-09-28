import logging
import os
import sys
import time

import psutil
from django.conf import settings
from django.core import management
from django.db.utils import OperationalError

HTTP_HOST = settings.HTTP_BIND_HOST or '127.0.0.1'
HTTP_PORT = settings.HTTP_LISTEN_PORT or 8080
CELERY_FLOWER_HOST = settings.CELERY_FLOWER_HOST or '127.0.0.1'
CELERY_FLOWER_PORT = settings.CELERY_FLOWER_PORT or 5555
DEBUG = settings.DEBUG or False
APPS_DIR = BASE_DIR = settings.BASE_DIR
LOG_DIR = os.path.join(BASE_DIR, 'logs')
TMP_DIR = os.path.join(LOG_DIR, 'tmp')

logger = logging.getLogger(__file__)


def check_database_connection():
    for i in range(60):
        logging.info(f"Check database connection: {i}")
        try:
            management.call_command('check', '--database', 'default')
            logging.info("Database connect success")
            return
        except OperationalError:
            logging.info('Database not setup, retry')
        except Exception as exc:
            logging.error('Unexpect error occur: {}'.format(str(exc)))
        time.sleep(1)
    logging.error("Connection database failed, exit")
    sys.exit(10)


def perform_db_migrate():
    logging.info("Check database structure change ...")
    logging.info("Migrate model change to database ...")
    try:
        management.call_command('migrate')
    except Exception as e:
        logging.error(f'Perform migrate failed, {e} exit', exc_info=True)
        sys.exit(11)


def collect_static():
    logging.info("Collect static files")
    try:
        management.call_command('collectstatic', '--no-input', '-c', verbosity=0, interactive=False)
        logging.info("Collect static files done")
    except:
        pass


def get_sys_thread_num():
    return psutil.cpu_count(False) if psutil.cpu_count(False) else 2


def get_sys_process_num():
    return psutil.cpu_count(True) if psutil.cpu_count(True) else 4


def prepare():
    check_database_connection()
    collect_static()
    perform_db_migrate()
