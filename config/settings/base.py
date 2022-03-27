from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# 기존 settings.py 파일의 위치는 /config인데 base.py 파일의 위치는 /config/settings로 하위 디렉토리로 이동하여 .parent를 한 번 더 사용하여 BASE_DIR을 설정
# /crsd/config/settings/base.py에서 총 세번의 .parent가 사용되었으므로 BASE_DIR은 결국 /crsd

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ls&1oied3t*np!^y6664m!j2-l%ie=8g$w-bjk_pjryzd#3y6b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['15.165.77.106']


# Application definition

INSTALLED_APPS = [              # 여기에 앱을 등록하고 나서 각 앱의 url.py를 사용하기위해 config/url.py파일도 수정해야 함
    'common.apps.CommonConfig', #  로그인 · 로그아웃을 '공통 기능을 가진 앱'이라는 의미의 common 앱
    'pybo.apps.PyboConfig',
    'django.contrib.admin',
    'django.contrib.auth',  # 장고의 로그인, 로그아웃을 도와주는 앱
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'raw_data' ,
        'USER': 'admin',
        'PASSWORD': 'qwerty1!',
        'HOST': 'csrd.cksngv0eixsu.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
}

    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',    
]

# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/'    # 로그인 성공 시 "/" 페이지로 이동할 수 있도록, config/urls.py 파일에 "/" 페이지에 대응하는 URL 매핑 추가

# 로그아웃시 이동하는 URL
LOGOUT_REDIRECT_URL = '/'   # 로그아웃 시 "/" 페이지로 이동하기 위해 LOGOUT_REDIRECT_URL을 설정
