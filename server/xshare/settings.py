"""
Django settings for xshare project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ftbwyk!&h-98rje2))(nb%7p#_(h&m9)s+a@5^r^#&varxvbhr"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'api.apps.ApiConfig',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'django_celery_results',
    'django_celery_beat'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "xshare.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "xshare.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xshare',
        'USER': 'xshare',
        'PASSWORD': 'KGzKjZpWBp4R4RSa',
        'HOST': 'mariadb',
        'PORT': 3306,
        'CONN_MAX_AGE': 600,
        # 设置MySQL的驱动
        # 'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
        'OPTIONS': {'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"', 'charset': 'utf8mb4'}
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'EXCEPTION_HANDLER': 'common.core.exception.common_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'common.core.throttle.LoginUserThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'LoginUser': '100/m',
        'UploadFile': '1000/m',
    },
    'DEFAULT_PAGINATION_CLASS': 'common.core.response.PageNumber',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # ),
}

# DRF扩展缓存时间
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 3600,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-token"
)

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,  # 在登录的时候更新user表  last_login 字段

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': 'x',
    'ISSUER': 'share',
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s/1" % ('redis', 6379),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": 'nineven',
            "DECODE_RESPONSES": True
        },
        "TIMEOUT": 60 * 15
    },
}

BASE_LOG_DIR = os.path.join(BASE_DIR, "logs", "api")
TMP_LOG_DIR = os.path.join(BASE_DIR, "logs", "tmp")

if not os.path.isdir(BASE_LOG_DIR):
    os.makedirs(BASE_LOG_DIR)
if not os.path.isdir(TMP_LOG_DIR):
    os.makedirs(TMP_LOG_DIR)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(funcName)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(funcName)s:%(lineno)d]%(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'TF': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，根据时间自动切
            'filename': os.path.join(BASE_LOG_DIR, "info.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 10,  # 备份数为3  xx.log --> xx.log.2018-08-23_00-00-00 --> xx.log.2018-08-24_00-00-00 --> ...
            # 'when': 'W6',  # 每天一切， 可选值有S/秒 M/分 H/小时 D/天 W0-W6/周(0=周一) midnight/如果没指定时间就默认在午夜
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "err.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "warning.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "sql.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {  # 默认的logger应用如下配置
            'handlers': ['TF', 'console', 'error', 'warning'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console', 'sql'],
            'propagate': True,
            'level': 'INFO',
        },
    },
}

CACHE_KEY_TEMPLATE = {
    'pending_state_key': 'pending_state',
    'upload_part_info_key': 'upload_part_info',
    'make_token_key': 'make_token',
    'drive_qrcode_key': 'drive_qrcode',
    'download_url_key': 'download_url',
    'aliyun_drive_auth_key': 'aliyun_drive_auth',
}

# Celery Configuration Options
# https://docs.celeryq.dev/en/stable/userguide/configuration.html?
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'

# broker redis
DJANGO_DEFAULT_CACHES = CACHES['default']
CELERY_BROKER_URL = 'redis://:%s@%s/2' % (
    DJANGO_DEFAULT_CACHES["OPTIONS"]["PASSWORD"], DJANGO_DEFAULT_CACHES["LOCATION"].split("/")[2])

CELERY_WORKER_CONCURRENCY = 10  # worker并发数
CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死
CELERY_RESULT_EXPIRES = 3600  # 任务结果过期时间

CELERY_WORKER_DISABLE_RATE_LIMITS = True  # 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
CELERY_WORKER_PREFETCH_MULTIPLIER = 60  # celery worker 每次去redis取任务的数量

CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000  # 每个worker执行了多少任务就会死掉，我建议数量可以大一些，比如200

CELERY_ENABLE_UTC = False
DJANGO_CELERY_BEAT_TZ_AWARE = True

# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'

# celery消息的序列化方式，由于要把对象当做参数所以使用pickle
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'

CELERY_BEAT_SCHEDULE = {
    'sync_drive_size_job': {
        'task': 'api.tasks.batch_sync_drive_size',
        'schedule': crontab(hour='2', minute='2'),
        'args': ()
    }, 'auth_clean_invalid_share_job': {
        'task': 'api.tasks.auth_clean_invalid_share',
        'schedule': crontab(hour='3', minute='3'),
        'args': ()
    }, 'clean_visitor_user_job': {
        'task': 'api.tasks.clean_visitor_user',
        'schedule': crontab(hour='2', minute='30'),
        'args': ()
    },
}

XSHARE = '__DO_NOT_DELETE_XSHARE__'
HTTP_BIND_HOST = '0.0.0.0'
HTTP_LISTEN_PORT = 8896
# celery flower 任务监控配置
CELERY_FLOWER_PORT = 5566
CELERY_FLOWER_HOST = '127.0.0.1'
# 设备指纹登录自动清理时间
TEMP_USER_CLEAN_TIME = timedelta(days=7)
