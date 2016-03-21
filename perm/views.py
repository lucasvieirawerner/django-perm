from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView

from .shortcuts import get_perm_queryset


class PermMixin(object):
    """
    Provide the ``has_perm`` interface to any object
    """
    perm = None

    def has_perm(self, object_or_model=None):
        """
        If a permission is set, the default result is False, else True
        """
        if self.perm:
            return False
        return True


class PermSingleObjectMixin(PermMixin):
    """
    Implement the PermMixin ``has_perm`` interface for Class Based Views with a get_object function.
    There is a special clause for CreateView instances.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        CreateView should check the permission based on the model class before doing anything else
        """
        if isinstance(self, CreateView):
            if not self.has_perm(self.model):
                raise PermissionDenied()
        return super(PermSingleObjectMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        """
        If an object is retrieved, check the users permission
        """
        obj = super(PermSingleObjectMixin, self).get_object(*args, **kwargs)
        if not self.has_perm(obj):
            raise PermissionDenied()
        return obj

    def has_perm(self, object_or_model=None):
        """
        If a permission is set, check the permission
        """
        if self.perm:
            return self.request.user.has_perm(self.perm, object_or_model)
        return True


class PermMultipleObjectMixin(PermMixin):
    """
    Implement the PermMixin ``has_perm`` interface for Class Based Views with a get_queryset function.
    """

    def get_queryset(self, *args, **kwargs):
        """
        Get the queryset with the proper permission
        """

        # QuerySet for permission
        perm_qs = get_perm_queryset(self.model, self.request.user, self.perm)

        try:
            # QuerySet for Class Based View
            super_qs = super(PermMultipleObjectMixin, self).get_queryset(*args, **kwargs)
        except AttributeError:
            # Not found? Use the permission queryset
            qs = perm_qs
        else:
            # Found? Filter it through permission queryset
            qs = super_qs.filter(pk__in=perm_qs)
        return qs


class PermDetailView(PermSingleObjectMixin, DetailView):
    """
    Implement the PermMixin ``has_perm`` interface for DetailView.
    """
    perm = 'view'


class PermUpdateView(PermSingleObjectMixin, UpdateView):
    """
    Implement the PermMixin ``has_perm`` interface for UpdateView.
    """
    perm = 'change'


class PermCreateView(PermSingleObjectMixin, CreateView):
    """
    Implement the PermMixin ``has_perm`` interface for CreateView.
    """
    perm = 'create'


class PermListView(PermMultipleObjectMixin, ListView):
    """
    Implement the PermMixin ``has_perm`` interface for ListView.
    """
    perm = 'list'


class PermDeleteView(PermSingleObjectMixin, DeleteView):
    """
    Implement the PermMixin ``has_perm`` interface for DeleteView.
    """
    perm = 'delete'
