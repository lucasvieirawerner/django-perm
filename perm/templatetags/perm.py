from __future__ import unicode_literals

import re

from django.db.models import Model
from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist

from ..utils import get_model_for_perm

QUOTED_STRING = re.compile(r'^["\'](?P<noquotes>.+)["\']$')

register = Library()


def handle_var(value, context):
    if not value:
        return None
    stringval = QUOTED_STRING.search(value)
    if stringval:
        return stringval.group('noquotes')
    else:
        try:
            return Variable(value).resolve(context)
        except VariableDoesNotExist:
            return value


@register.assignment_tag(takes_context=True)
def perm(context, perm, obj_or_model=None):
    perm = handle_var(perm, context)
    model = handle_var(obj_or_model, context)
    if model and not isinstance(model, Model):
        model = get_model_for_perm(model, raise_exception=True)
    try:
        request = context['request']
    except KeyError:
        raise TemplateSyntaxError("Tag '%(tag)' requires request context".format(tag=tag))
    try:
        user = request.user
    except AttributeError:
        raise TemplateSyntaxError("Tag '%(tag)' requires attribute 'user' in request context".format(tag=tag))
    if model:
        return user.has_perm(perm, model)
    return user.has_perm(perm)
