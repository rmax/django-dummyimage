DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

DUMMYIMAGE_MAX_DIMENSION = 1024

ROOT_URLCONF = 'dummyimage.urls'

INSTALLED_APPS = (
    'dummyimage',
)

