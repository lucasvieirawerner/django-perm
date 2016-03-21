# Get get_model across Django versions
try:
    from django.apps import apps

    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

# Get basestring across Python versions
try:
    # Python 2
    string_types = (basestring, )
except NameError:
    # Python 3
    string_types = (str, )
