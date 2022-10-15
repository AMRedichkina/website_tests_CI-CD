import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%6+q7+@3wm_07(#8x#i*ps$2f$v1lheet_o&(tyy12ugh04tv7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'testserver',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'sorl.thumbnail',
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

ROOT_URLCONF = 'yatube.urls'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.year.year',
            ],
        },
    },
]

WSGI_APPLICATION = 'yatube.wsgi.application'

CSRF_FAILURE_VIEW = 'core.views.csrf_failure'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'posts:index'
# LOGOUT_REDIRECT_URL = 'posts:index'

# Константы (иные)
POSTS_PER_PAGE = 10

# Эмуляция почтового сервера
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

# Кэш
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Переменные (в основном для тестов)
# name
NAME_INDEX = 'posts:index'
NAME_PROFILE = 'posts:profile'
NAME_POST_DETAIL = 'posts:post_detail'
NAME_GROUP_LIST = 'posts:group_list'
NAME_POST_CREATE = 'posts:post_create'
NAME_POST_EDIT = 'posts:post_edit'
NAME_FOLLOWER = 'posts:profile_follow'
NAME_FOLLOWER_INDEX = 'posts:follow_index'
NAME_UNFOLLOWER = 'posts:profile_unfollow'
NAME_ADD_COMMENT = 'posts:add_comment'

# html
HTML_INDEX = 'posts/index.html'
HTML_PROFILE = 'posts/profile.html'
HTML_POST_DELAIL = 'posts/post_detail.html'
HTML_GROUP_LIST = 'posts/group_list.html'
HTML_POST_CREATE = 'posts/create_post.html'
HTML_POST_EDIT = 'posts/create_post.html'
HTML_404 = 'core/404.html'
HTML_403 = 'core/403.html'
HTML_CSRF = 'core/403csrf.html'
HTML_500 = 'core/500.html'

# url
URL_INDEX = '/'
URL_PROFILE = '/profile/auth/'
URL_POST_DETAIL = '/posts/1/'
URL_GROUP_LIST = '/group/test-slug/'
URL_POST_CREATE = '/create/'
URL_POST_EDIT = '/posts/1/edit/'
