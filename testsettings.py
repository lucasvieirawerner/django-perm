from django.conf import global_settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

SECRET_KEY = 'ishalltellyouonlyonce'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'perm',
)

# Add perm to authentication backends
AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + [
    # Object permissions using perm
    'perm.backends.ModelPermissionBackend',
]

# Django >= 1.7 complains if this is not set
MIDDLEWARE_CLASSES = global_settings.MIDDLEWARE_CLASSES

# Django >= 1.10 requires TEMPLATES setting
# See https://docs.djangoproject.com/en/1.9/ref/templates/upgrading/#the-templates-settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
