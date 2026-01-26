import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR))

sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

SECRET_KEY = "django-insecure-fe66yaw7i$2^s3d=z6+8v#*#q-(xcrt28fw=yh13@%&7cr%l#y" # 盐

DEBUG = True
# DEBUG = False

# ALLOWED_HOSTS = [] # 开发时默认空，只允许 localhost
ALLOWED_HOSTS = ['*']  # 允许所有 IP/域名访问（群晖部署常用，方便内网/外网访问）

# ALLOWED_HOSTS = [
#     'hq-oms.com',  # 唯一允许访问后端的域名（无其他地址）
#     # 可选：若需要用服务器公网IP访问（比如调试），可加IP，否则不加
#     # '123.45.67.89',
# ]
#
# # 2. CORS配置：只允许这个域名的前端跨域请求（因为前端也在这个域名下）
# CORS_ALLOWED_ORIGINS = [
#     "https://hq-oms.com",  # 唯一允许跨域的前端地址
# ]

# 允许跨域
CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",  # DRF-API
    "corsheaders",  # 跨域
    "machine",
    "order",
    "sample",
    "process",
    "analysis",
    "market",
    "sync",
    "user",
]

# 允许Cookie
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS中间件（处理跨域请求，需放最前面）
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware", # CSRF 防护中间件（前后端分离项目常用）
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "HQ_OMS.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "HQ_OMS.wsgi.application"

# 本地数据库配置
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": 'hq_oms',
        "USER": 'root',
        "PASSWORD": '123456',
        "HOST": 'localhost',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# 群辉docker数据库配置
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv('DATABASE_NAME', 'hq_oms'),  # 数据库名，与 docker-compose 一致
#         'USER': os.getenv('DATABASE_USER', 'root'),    # MySQL 默认用户 root
#         'PASSWORD': os.getenv('DATABASE_PASSWORD', '123456'),  # 密码，与 docker-compose 一致
#         'HOST': os.getenv('DATABASE_HOST', 'hq_oms_mysql'),      # Docker MySQL 服务名，严禁改 IP/localhost
#         'PORT': os.getenv('DATABASE_PORT', '3306'),    # MySQL 默认端口
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#             'sql_mode': 'STRICT_TRANS_TABLES'  # 适配 MySQL 8.0，避免报错
#         }
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = False

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
