from __future__ import unicode_literals

from django.conf import settings as django_settings

PERM_DEFAULT_SETTINGS = {
    'cache': {
        'name': 'default',
        'expires': 60,
    }
}

perm_settings = PERM_DEFAULT_SETTINGS.copy()
perm_settings.update(getattr(django_settings, 'PERM_SETTINGS', {}))
