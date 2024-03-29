import os
from pathlib import Path


import pyrebase


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bd^y$57qcs6wn91=_=gm0z-90*$zvslm6qfdn(s8qj3fajj-e_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [] 

#CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'https://editor.swagger.io', 
    'http://editor.swagger.io'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'document_Api',
    'corsheaders',
] 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
    'django.middleware.gzip.GZipMiddleware', 
]

ROOT_URLCONF = 'document_management_API.urls'

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

WSGI_APPLICATION = 'document_management_API.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'IMAGES', 
        'ENFORCE_SCHEMA': False, 
        'CLIENT': {
            'host': 'mongodb://localhost:27017/',  # Update with your MongoDB connection string 
            
        }
        
    }
} 

# Cache mechanisms
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',  # Adjust the host, port, and database number as needed
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Set session timeout in seconds (e.g., 15 minutes)
SESSION_COOKIE_AGE = 900

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Database-backed sessions
SESSION_COOKIE_NAME = 'my_session_cookie'  # Custom session cookie name 
SESSION_SAVE_EVERY_REQUEST = True


# Firebase cloud storage credentials
FIERBASE_CONFIG = {
  "apiKey": "AIzaSyCRomgiZX1macZNHeJsthtfU_ia9oftiNk",
  'authDomain': "documentmanagement-32846.firebaseapp.com",
  'projectId': "documentmanagement-32846",
  'storageBucket': "documentmanagement-32846.appspot.com",
  'messagingSenderId': "31201439126",
  'appId': "1:31201439126:web:333096e492d54a280d01b7",
  'measurementId': "G-MMWBQDNZG6",  
  'databaseURL': "https://documentmanagement-32846-default-rtdb.firebaseio.com/",
  'serviceAccount': "serviceAccount.json",  
}

# config with firebase
firebase = pyrebase.initialize_app(FIERBASE_CONFIG ) 
 
# get storage instance 
storage = firebase.storage() 
