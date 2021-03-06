from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from perm.cache import cache_get, cache_set, cache_key
from .exceptions import PermAppException, PermQuerySetNotFound, PermMethodNotFound, PermPrimaryKeyNotFound
from .utils import get_model_for_perm


class ModelPermissionsManager(object):
    """
    Singleton object to hold ModelPermissions classes for objects
    """
    _registry = {}

    def register(self, model, permissions_class):
        model = get_model_for_perm(model)
        self._registry[model] = permissions_class
        return model

    def register_permissions_class(self, permissions_class, model):
        self.register(model, permissions_class)
        return permissions_class

    def get_permissions(self, model, user_obj, perm, obj=None, raise_exception=False):
        model = get_model_for_perm(model)
        permissions_checker_class = self._registry.get(model, None)
        if not permissions_checker_class:
            if raise_exception:
                raise PermAppException(_('No permissions registered for %(model)s.' % {'model': model}))
            return None
        permissions = permissions_checker_class(model, user_obj, perm, obj)
        return permissions


class ModelPermissions(object):
    """
    Class is instantiated once a permission has to be checked.
    The check itself is done by calling the has_perm() method.
    """
    model = None
    user = None
    perm = None
    obj = None

    allow_anonymous_user = False
    allow_inactive_user = False

    def __init__(self, model, user_obj, perm, obj=None, *args, **kwargs):
        """
        Set the properties
        """
        super(ModelPermissions, self).__init__()
        self.model = model
        self.user = user_obj
        self.obj = obj
        self.perm = perm

    def get_cache_key(self):
        """
        Get a unique cache key for this object's parameters
        """
        return cache_key(
            model=self.model,
            user=self.user,
            obj=self.obj,
            perm=self.perm,
        )

    def get_queryset(self):
        """
        Get method get_queryset_perm_PERM or return None
        """
        try:
            method = getattr(self, 'get_queryset_perm_%s' % self.perm)
        except AttributeError:
            raise PermQuerySetNotFound(_('Permissions for %(model)s do not include queryset for %(perm)s.' % {
                'model': self.model,
                'perm': self.perm
            }))
        # No need for self parameter, Python knows it is a method
        return method()

    def _has_perm_using_method(self):
        """
        Test the method has_perm_PERM()
        """
        try:
            method = getattr(self, 'has_perm_%s' % self.perm)
        except AttributeError:
            raise PermMethodNotFound(_('Permissions for %(model)s do not include method for %(perm)s.' % {
                'model': self.model,
                'perm': self.perm
            }))
        # No need for self parameter, Python knows it is a method
        return method()

    def _has_perm_using_queryset(self):
        """
        Test to see if obj appears in get_perm_PERM_queryset()
        """

        # Get the queryset (raises PermQuerySetNotFound if not available)
        qs = self.get_queryset()

        # Get the PK (raise PermPrimaryKeyNotFound if not available)
        try:
            pk = self.obj.pk
        except AttributeError:
            raise PermPrimaryKeyNotFound(
                _('Permission {perm} for object {object} (model {model}) requires a primary key.'.format(
                    object=self.obj,
                    perm=self.perm,
                    model=self.model,
                ))
            )

        # Math the object with the queryset
        return qs.filter(pk=pk).exists()

    def _has_perm(self):
        """
        Test using direct method and queryset
        """

        # Check empty, anonymous and inactive users
        if not self.allow_anonymous_user or not self.allow_inactive_user:
            if not self.user or self.user.pk is None:
                return False
            if not self.allow_inactive_user and not self.user.is_active:
                return False

        # Try using method, move on if no method is defined
        try:
            return self._has_perm_using_method()
        except PermMethodNotFound:
            pass

        # Try using queryset, forgive lacking QS or PK by eventually returning False
        try:
            return self._has_perm_using_queryset()
        except (PermQuerySetNotFound, PermPrimaryKeyNotFound):
            pass

        # Deny permission
        return False

    def has_perm(self):
        """
        Test for permission
        """
        cache_key = self.get_cache_key()
        result = cache_get(cache_key)
        if result is None:
            result = self._has_perm()
            cache_set(cache_key, result)
        return result


# Instantiate the singleton
permissions_manager = ModelPermissionsManager()
