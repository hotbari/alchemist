
from pathlib import Path
import environ
from datetime import timedelta
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# environ 초기화
env = environ.Env(
    # 캐스팅 및 기본값 설정
    DEBUG=(bool, True),
    SECRET_KEY=(str, 'your-default-secret-key'),  # 기본값 예시
    # AWS_ACCESS_KEY_ID=(str, 'your-default-access-key'),
    # AWS_SECRET_ACCESS_KEY=(str, 'your-default-secret-access-key'),
    # AWS_STORAGE_BUCKET_NAME=(str, 'your-default-bucket-name'),
)


# .env 파일 동적으로 찾기
env_file_path = BASE_DIR / '.env'
if os.path.isfile(env_file_path):
    env.read_env(str(env_file_path))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')


ALLOWED_HOSTS = ['*'] # postman 테스트를 위해 *로 잠시 세팅



# AWS settings
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'



# Application definition

CUSTOM_APPS = [
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'coach.apps.CoachConfig',
    'team.apps.TeamConfig',
    'club.apps.ClubConfig',
    'tier.apps.TierConfig',
    'image_url.apps.ImageUrlConfig',
    'matchtype.apps.MatchTypeConfig',
]


SYSTEM_APPS = [
    'corsheaders',
    'competition.apps.CompetitionConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangorestframework_camel_case',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
]

INSTALLED_APPS = CUSTOM_APPS + SYSTEM_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # <- 가능한 높게 위치시켜야 한다.
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangorestframework_camel_case.middleware.CamelCaseMiddleWare',
]

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
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'


# 원하는 타임존 설정
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Auth 기본값 설정
AUTH_USER_MODEL = 'users.CustomUser'


# jwt
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
     'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser', # 카멜 케이스 변환 파서
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer', # 최상위로 올려야 카멜케이스로 변경 가능
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer', # 최상위로 올려야 카멜케이스 변경 가능
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

SIMPLE_JWT = {
    'TOKEN_OBTAIN_SERIALIZER': 'users.serializers.CustomTokenObtainPairSerializer',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'TOKEN_USER_CLASS': 'users.CustomUser',
    'ALGORITHM': 'HS256',
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    'SIGNING_KEY': env('SIMPLE_JWT_SIGNING_KEY', default=None) or SECRET_KEY,
}


CORS_ORIGIN_ALLOW_ALL = True # <- 모든 호스트 허용
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CSRF_TRUSTED_ORIGINS = [
    'https://alchemistapi.watcher.team',
]