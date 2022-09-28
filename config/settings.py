"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import cloudinary

from datetime import timedelta
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    # Admin Template
    'jazzmin',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Frameworks
    'corsheaders',
    'ckeditor',
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'cloudinary',
    'phonenumber_field',

    # My Apps
    'user.apps.UserConfig',
    'advertisement.apps.AdvertisementConfig',
    'siteapp.apps.SiteAppConfig',
    'chat.apps.ChatConfig',
    'social_auth.apps.SocialAuthConfig',
    'payment.apps.PaymentConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "config.middleware.JWTAuthMiddleware",
    "config.middleware.IPMiddleware",
    "config.middleware.RequestLimitMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "config.middleware.ViewMiddleware"
]

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'filters': {
#         'filter_info_level': {
#             '()': 'config.log_middleware.FilterLevels',
#             'filter_levels': [
#                 "INFO"
#             ]
#         },
#         'filter_error_level': {
#             '()': 'config.log_middleware.FilterLevels',
#             'filter_levels': [
#                 "ERROR"
#             ]
#         },
#         'filter_warning_level': {
#             '()': 'config.log_middleware.FilterLevels',
#             'filter_levels': [
#                 "WARNING"
#             ]
#         }
#     },
#     'formatters': {
#         'info-formatter': {
#             'format': '%(levelname)s : %(message)s - [in %(pathname)s:%(lineno)d]'
#         },
#         'error-formatter': {
#             'format': '%(levelname)s : %(asctime)s {%(module)s} [%(funcName)s] %(message)s- [in %(pathname)s:%(lineno)d]',
#             'datefmt': '%Y-%m-%d %H:%M'
#         },
#         'short': {
#             'format': '%(levelname)s : %(message)s'
#         }
#     },
#     'handlers': {
#         'customHandler_1': {
#             'formatter': 'info-formatter',
#             'class': 'config.log_middleware.DatabaseLoggingHandler',
#             'database': 'config',
#             'collection': 'logs',
#             'filters': ['filter_info_level'],
#         },
#         'customHandler_2': {
#             'formatter': 'error-formatter',
#             'class': 'config.log_middleware.DatabaseLoggingHandler',
#             'database': 'config',
#             'collection': 'logs',
#             'filters': ['filter_error_level'],
#         },
#         'customHandler_3': {
#             'formatter': 'short',
#             'class': 'logging.StreamHandler',
#             'filters': ['filter_warning_level'],
#         },
#     },
#     'loggers': {
#         'customLogger': {
#             'handlers': [
#                 'customHandler_1',
#                 'customHandler_2',
#                 'customHandler_3'
#             ],
#             'level': 'DEBUG',
#         },
#     },
# }

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#
#     'formatters': {
#         'main_formatter': {
#             'format': '%(message)s - %(asctime)s [%(levelname)s]'
#         },
#     },
#
#     'handlers': {
#         # 'console': {
#         #     'class': 'logging.StreamHandler',
#         #     'formatter': 'main_formatter',
#         # },
#         'debug': {
#             'class': 'logging.FileHandler',
#             'filename': 'log/dubug.log',
#             'formatter': 'main_formatter',
#             'level': 'DEBUG'
#         },
#         'error': {
#             'class': 'logging.FileHandler',
#             'filename': 'log/error.log',
#             'formatter': 'main_formatter',
#             'level': 'ERROR'
#         },
#         'info': {
#             'class': 'logging.FileHandler',
#             'filename': 'log/info.log',
#             'formatter': 'main_formatter',
#             'level': 'INFO'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': [
#                 # 'console',
#                 'error',
#                 'info',
#                 'debug'
#             ],
#             'propagate': True,
#             'level': 1,
#         },
#     },
# }

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'user.User'
# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

LOGIN_REDIRECT_URL = '/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF Config
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,

    # 'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    # ),
    "DATE_INPUT_FORMATS": ["%d.%m.%Y"],
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

JWT_CONFIG = {
    'TOKEN_LIFETIME': timedelta(minutes=60),
    'AUTH_HEADER_TYPES': 'Bearer',

    'SIGNING_KEY': SECRET_KEY,
    'ALGORITHM': 'HS256',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
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

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "BAZAR Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Bazar",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Bazar",

    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "books/img/logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the admin panel",

    # Copyright on the footer
    "copyright": "GG",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": AUTH_USER_MODEL,

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://t.me/baha996", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        # {"app": "books"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://t.me/baha996", "new_window": True},
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    # "order_with_respect_to": ["auth", "books", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "books": [{
    #         "name": "Make Messages",
    #         "url": "make_messages",
    #         "icon": "fas fa-comments",
    #         "permissions": ["books.view_book"]
    #     }]
    # },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    # "language_chooser": True,
}

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_LOGIN')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
EMAIL_USE_TLS = True

# Cloudinary config
cloudinary.config(
    cloud_name=config('CLOUD_NAME'),
    api_key=config('CLOUD_API_KEY'),
    api_secret=config('CLOUD_API_SECRET')
)

CORS_ORIGIN_ALLOW_ALL = True

# Redis config
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')

# Celery config
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", f"redis://{REDIS_HOST}:{REDIS_PORT}/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", f"redis://{REDIS_HOST}:{REDIS_PORT}/0")
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': int(config('CELERY_OPTIONS_VISIBILITY_TIMEOUT'))}
CELERY_ACCEPT_CONTENT = [config('CELERY_ACCEPT_CONTENT_APPLICATION')]
CELERY_TASK_SERIALIZER = config('CELERY_TASK_SERIALIZER')
CELERY_RESULT_SERIALIZER = config('CELERY_RESULT_SERIALIZER')

# Pusher config
PUSHER_APP_ID = config('PUSHER_APP_ID')
PUSHER_KEY = config('PUSHER_KEY')
PUSHER_SECRET = config('PUSHER_SECRET')
PUSHER_CLUSTER = config('PUSHER_CLUSTER')
PUSHER_SSL = bool(config('PUSHER_SSL'))

# Advertisement choices
ACTIVE = 'Активный'
CHECKING = 'На проверке'
DISABLE = 'Неактивный'

ADS_CHOICES = (
    (ACTIVE, ACTIVE),
    (CHECKING, CHECKING),
    (DISABLE, DISABLE)
)

# SiteApp choices
SOCIAL_NETWORK = 'Social Networks'
APP = 'App'

SOCIAL_MEDIA = (
    (SOCIAL_NETWORK, SOCIAL_NETWORK),
    (APP, APP)
)

CLAIM = 'жалоба'
OFFER = 'предложение'

SUBJECT = (
    (CLAIM, CLAIM),
    (OFFER, OFFER)
)

GOOGLE = 'google'
FACEBOOK = 'facebook'

AUTH_TYPE = (
    (GOOGLE, GOOGLE),
    (FACEBOOK, FACEBOOK)
)

WRONG_RUBRIC = 'Неверная рубрика'
BANNED_GOODS_OR_SERVICE = 'Запрещенный товар/услуга'
NOT_ACTUAL = 'Объявление не актуально'
WRONG_ADDRESS = 'Неверный адрес'
OTHER = 'Другое'

COMPLAINING_TYPE = (
    (WRONG_RUBRIC, WRONG_RUBRIC),
    (BANNED_GOODS_OR_SERVICE, BANNED_GOODS_OR_SERVICE),
    (NOT_ACTUAL, NOT_ACTUAL),
    (WRONG_ADDRESS, WRONG_ADDRESS),
    (OTHER, OTHER),
)

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'width': '100%',

    }
}

# PayBox config
PAYBOX_URL = "https://api.paybox.money/payment.php"
PAYBOX_PROJECT_ID = config("PAYBOX_PROJECT_ID")
PAYBOX_SECRET_KEY = config("PAYBOX_SECRET_KEY")

CURRENT_URL = config("CURRENT_URL")
PAYBOX_SALT = config("PAYBOX_SALT")
PAYBOX_SUCCESS_URL_METHOD = config("PAYBOX_SUCCESS_URL_METHOD")
PAYBOX_CURRENCY = "KGS"
PAYBOX_LANGUAGE = "ru"
PAYBOX_SUCCESS_URL = f"{CURRENT_URL}"
PAYBOX_RESULT_URL = config("PAYBOX_RESULT_URL")