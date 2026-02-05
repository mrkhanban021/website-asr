
from pathlib import Path
import os
import environ


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / '.env.prod'
env = environ.Env()

if ENV_FILE.exists():
    environ.Env.read_env(ENV_FILE)


SECRET_KEY = env('SECRET_KEY')


DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'meta',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'identify.apps.IdentifyConfig',
    'website.apps.WebsiteConfig',
]



AUTH_USER_MODEL = 'identify.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.utils.context_processors.default_meta',
                'core.utils.context_processors.get_global_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env.int('DB_PORT'),
        'CONN_MAX_AGE': env.int('DB_CONN_MAX_AGE'),
        'OPTIONS': {
            'connect_timeout': env.int('DB_CONN_TIMEOUT'),
        }

    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env('DJANGO_CACHE_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,
        },
        "KEY_PREFIX": "site_asr",
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR / 'static')

STATICFILES_DIRS = [
    BASE_DIR / 'assets'
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR / "media")


META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = 'asr-elevator.ir'
META_SITE_NAME = 'آریان سیستم رو'
META_SITE_TYPE = 'website'
META_DEFAULT_TITLE = 'آریان سیستم رو'
META_DEFAULT_DESCRIPTION = 'آریان سیستم رو تولید کننده درب تمام اتوماتیک آسانسور'
META_DEFAULT_KEYWORDS = ['درب آسانسور', 'درب طبقه آسانسور راد پلاس', 'درب طبقه آسانسور سلکوم پلاس',
                         'قطعات یدکی درب آسانسور', 'بهترین درب آسانسور', 'سلکوم', 'سلکوم پلاس', 'راد', 'رادپلاس', 'ایران']
META_DEFAULT_IMAGE = '/static/images/favicon.png'
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = [
    'email*',
    'password1*',
    'password2*',
]
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_ADAPTER = 'identify.adapters.MySocialAccountAdapter'
SOCIALACCOUNT_AUTO_SIGNUP = True


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    }
}


