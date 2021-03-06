class PermException(Exception):
    """
    Something goes wrong within perm
    """
    pass


class PermAppException(PermException):
    """
    Something goes wrong within perm, but it it something that might happen because of they way the app works
    """
    pass


class PermQuerySetNotFound(PermAppException):
    """
    The queryset we were looking for was not found
    """
    pass


class PermMethodNotFound(PermAppException):
    """
    The method we were looking for was not found
    """
    pass


class PermPrimaryKeyNotFound(PermAppException):
    """
    The instance we are evaluating has no primary key
    """
    pass
