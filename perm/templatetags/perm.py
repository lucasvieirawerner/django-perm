from __future__ import unicode_literals

from django.db.models import Model
from django.template import Library, TemplateSyntaxError

from ..utils import get_model_for_perm

register = Library()


@register.assignment_tag(takes_context=True)
def perm(context, action, obj_or_model=None):
    tag = 'perm'
    if obj_or_model and not isinstance(obj_or_model, Model):
        obj_or_model = get_model_for_perm(obj_or_model, raise_exception=True)
    try:
        request = context['request']
    except KeyError:
        raise TemplateSyntaxError("Tag '%(tag)' requires request context".format(tag=tag))
    try:
        user = request.user
    except AttributeError:
        raise TemplateSyntaxError("Tag '%(tag)' requires attribute 'user' in request context".format(tag=tag))
    if obj_or_model:
        return user.has_perm(action, obj_or_model)
    return user.has_perm(action)
