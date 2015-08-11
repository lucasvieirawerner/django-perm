from .permissions import permissions_manager


def permissions_for(model):
    """
    Decorator for permissions class, to automatically register it for a given model
    """
    def wrap(permissions_class):
        permissions_manager.register(model, permissions_class)
        return permissions_class

    return wrap
