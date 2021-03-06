from __future__ import unicode_literals

from unittest import TestCase

from django.contrib.auth.models import User
from django.db import models
from django.template import Template, Context
from django.utils.encoding import python_2_unicode_compatible

from .decorators import permissions_for
from .exceptions import PermAppException
from .permissions import ModelPermissions
from .utils import get_model_for_perm

# Dummy patterns to satisfy Django
urlpatterns = ()


@python_2_unicode_compatible
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def user_can_visit(self, user):
        return user.is_staff

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name).strip()


@permissions_for(Person)
class PersonPermissions(ModelPermissions):
    def has_perm_create(self):
        # Only superuser can create
        return self.user.is_superuser

    def has_perm_visit(self):
        # Let's ask the Person object
        return self.obj.user_can_visit(self.user)

    def get_queryset_perm_gamma(self):
        # Permission gamma can only be tested by queryset and will not work on Model Class
        if self.user.username == 'gamma' or self.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.none()


class MockRequest(object):
    pass


def get_request_for_user(user):
    request = MockRequest()
    request.user = user
    return request


def render_template(template, **context_args):
    """
    Create a template that loads perm. Result is stripped of whitespace.
    """
    template = Template("{% load perm %}" + template)
    return template.render(Context(context_args)).strip()


class UtilsTest(TestCase):
    def test_get_model(self):
        with self.assertRaises(PermAppException):
            get_model_for_perm('does.NotExist', raise_exception=True)
        self.assertEqual(None, get_model_for_perm('does.NotExist', raise_exception=False))
        self.assertEqual(Person, get_model_for_perm('perm.Person', raise_exception=False))


class PermissionsTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(first_name='alpha', last_name='centauri')
        self.superuser = User.objects.create(username='alpha', is_superuser=True, is_staff=False)
        self.staff_user = User.objects.create(username='beta', is_superuser=False, is_staff=True)
        self.normal_user = User.objects.create(username='gamma', is_superuser=False, is_staff=False)

    def test_permission_does_not_exist(self):
        perm = 'does_not_exist'
        # True for superuser
        self.assertEqual(True, self.superuser.has_perm(perm))
        self.assertEqual(True, self.superuser.has_perm(perm, Person))
        self.assertEqual(True, self.superuser.has_perm(perm, self.person))
        # False for non-superusers
        self.assertEqual(False, self.staff_user.has_perm(perm))
        self.assertEqual(False, self.staff_user.has_perm(perm, Person))
        self.assertEqual(False, self.staff_user.has_perm(perm, self.person))

    def test_permission_create(self):
        perm = 'create'
        # True for superuser
        self.assertEqual(True, self.superuser.has_perm(perm))
        self.assertEqual(True, self.superuser.has_perm(perm, Person))
        self.assertEqual(True, self.superuser.has_perm(perm, self.person))
        self.assertEqual(True, self.superuser.has_perm(perm, 'perm.Person'))
        # False for our staff user
        self.assertEqual(False, self.staff_user.has_perm(perm))
        self.assertEqual(False, self.staff_user.has_perm(perm, Person))
        self.assertEqual(False, self.staff_user.has_perm(perm, self.person))
        self.assertEqual(False, self.staff_user.has_perm(perm, 'perm.Person'))

    def test_permission_gamma(self):
        perm = 'gamma'
        # True for superuser
        self.assertEqual(True, self.superuser.has_perm(perm))
        self.assertEqual(True, self.superuser.has_perm(perm, Person))
        self.assertEqual(True, self.superuser.has_perm(perm, self.person))
        # False for our staff user, since he is not named gamma
        self.assertEqual(False, self.staff_user.has_perm(perm))
        self.assertEqual(False, self.staff_user.has_perm(perm, Person))
        self.assertEqual(False, self.staff_user.has_perm(perm, self.person))
        # True for our normal user, since he is named gamma
        self.assertEqual(True, self.normal_user.has_perm(perm, self.person))
        # Except when we give a model class, because it works on querysets only
        self.assertEqual(False, self.normal_user.has_perm(perm, Person))
        # Except without an object, then the result will be False
        self.assertEqual(False, self.normal_user.has_perm(perm))

    def test_template_tag_perm(self):
        # Inner function to test a template
        def _test_template(user, perm):
            request = get_request_for_user(user)
            template = '{{% perm "{perm}" person as var %}}{{{{ var }}}}'.format(perm=perm)
            return render_template(template, request=request, person=self.person)

        self.assertEqual('alpha centauri', render_template('{{ person }}', request={'user': None}, person=self.person))
        self.assertEqual('True', _test_template(self.superuser, 'does_not_exist'))
        self.assertEqual('False', _test_template(self.staff_user, 'does_not_exist'))
        self.assertEqual('True', _test_template(self.superuser, 'gamma'))
        self.assertEqual('False', _test_template(self.staff_user, 'gamma'))
        self.assertEqual('True', _test_template(self.normal_user, 'gamma'))

    def tearDown(self):
        self.superuser.delete()
        self.staff_user.delete()
        self.normal_user.delete()
        self.person.delete()
