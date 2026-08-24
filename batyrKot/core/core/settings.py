import os
from pathlib import Path

# Корневая папка проекта — теперь это папка "книжный-магазин", а не core
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Безопасность (для разработки)
SECRET_KEY = 'django-insecure-8#_&@2%8w!q$9x7b6f5g4h3j2k1l0m9n8o7p6q5r4s3t2u1v0w9x8y7z'
DEBUG = True
ALLOWED_HOSTS = ['my-book-shop-z7cj.onrender.com', 'localhost', '127.0.0.1', '*']

# ------------------------------------------------------------
# Приложения
# ------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Наши приложения (порядок важен)
    'shop',
    'users',
    'cart',
    'orders',

    # Сторонние
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# ------------------------------------------------------------
# Промежуточные слои
# ------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- Добавить сюда!
]

# ------------------------------------------------------------
# Корневой URL-конфиг
# ------------------------------------------------------------
ROOT_URLCONF = 'core.urls'

# ------------------------------------------------------------
# Шаблоны — теперь ищет в книжный-магазин/templates
# ------------------------------------------------------------
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
                'cart.context_processors.cart_total',
                'shop.context_processors.categories_nav',
            ],
        },
    },
]

# ------------------------------------------------------------
# WSGI
# ------------------------------------------------------------
WSGI_APPLICATION = 'core.wsgi.application'

# ------------------------------------------------------------
# База данных — теперь db.sqlite3 лежит в книжный-магазин/
# ------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------------------------------------
# Валидация паролей
# ------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------
# Локализация
# ------------------------------------------------------------
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------
# Статика и медиа — теперь в книжный-магазин/static и книжный-магазин/media
# ------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------------------
# Аутентификация
# ------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# ------------------------------------------------------------
# Stripe (для оплаты)
# ------------------------------------------------------------
STRIPE_PUBLISHABLE_KEY = 'pk_test_...'
STRIPE_SECRET_KEY = 'sk_test_...'

# ------------------------------------------------------------
# По умолчанию
# ------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
