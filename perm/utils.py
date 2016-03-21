from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from perm.compat import string_types, get_model
from .exceptions import PermAppException


def get_model_for_perm(model, raise_exception=False):
    """
    Get the model for a given object or class.
    If ``raise_exception`` is set to True, an Exception is raised if no class can be found.
    If ``raise_exception`` is set to False (default), ``None`` is a valid result.
    """
    if isinstance(model, string_types):
        # If model is a string, find the appropriate model class
        try:
            app_name, model_name = model.split('.')
        except ValueError:
            model_class = None
        else:
            try:
                model_class = get_model(app_name, model_name)
            except LookupError:
                model_class = None
    else:
        # Assume we have been given a model class or instance
        model_class = model

    # Handle failure
    if not model_class:
        if raise_exception:
            raise PermAppException(_('%(model)s is not a Django Model class.' % {
                'model': model
            }))
        return None

    # Return the result
    return model_class
