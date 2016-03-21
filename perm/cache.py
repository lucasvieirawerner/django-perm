from __future__ import unicode_literals

import hashlib

from .conf import perm_settings

from django.core.cache import caches

_cache_settings = perm_settings['cache']
_cache_name = _cache_settings['name']
_cache_expires = _cache_settings['expires']
_cache = caches[_cache_name]


def cache_get(key, default=None):
    """
    Get a value from the cache (default if not available)
    """
    return _cache.get(key, default)


def cache_set(key, value):
    """
    Set a value in the cache
    """
    return _cache.set(key, value, _cache_expires)


def cache_key(**kwargs):
    """
    Return an md5 hash of all kwargs, sorted by key name. No args allowed.
    """
    parts = []
    for key in sorted(kwargs):
        parts.append('{key}:{value}'.format(key=key, value=kwargs[key]))
    hash_object = hashlib.md5('-'.join(parts).encode())
    hash_string = hash_object.hexdigest()
    # Prepend PERM for clarity
    return 'PERM-{hash_string}'.format(hash_string=hash_string)
