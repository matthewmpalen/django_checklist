# Django
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

# External
from rest_framework.test import APITestCase

# Local
from django_checklist.common.models import Tag
from django_checklist.todo.models import Checklist, Item

def _get_ctypes():
    """
    Returns a dictionary of class names and ContentTypes
    """
    output = {}
    models = [Tag, Checklist, Item]

    for ctype in models:
        output[ctype.__name__] = ContentType.objects.get_for_model(ctype)

    return output

def _get_permissions():
    """
    Returns nested dictionary of class names and Permissions
    """
    output = {}
    for cname, ctype in _get_ctypes().items():
        add_codename = 'add_{0}'.format(cname.lower())
        change_codename = 'change_{0}'.format(cname.lower())
        delete_codename = 'delete_{0}'.format(cname.lower())

        add_perm = Permission.objects.get(content_type=ctype, 
            codename=add_codename)
        change_perm = Permission.objects.get(content_type=ctype, 
            codename=change_codename)
        delete_perm = Permission.objects.get(content_type=ctype, 
            codename=delete_codename)

        perms = {
            'add': add_perm, 
            'change': change_perm, 
            'delete': delete_perm
        }

        output[cname] = perms

    return output

class PermissionsTestCaseMixin(object):
    """
    Initializes Group permissions for testing
    """

    def initialize(self):
        self.basic_group = Group.objects.create(name='Basic')

        perms = _get_permissions()
        # Basic
        self.basic_group.permissions.add(perms[Tag.__name__]['add'])
        self.basic_group.permissions.add(perms[Checklist.__name__]['add'])
        self.basic_group.permissions.add(perms[Checklist.__name__]['change'])
        self.basic_group.permissions.add(perms[Checklist.__name__]['delete'])
        self.basic_group.permissions.add(perms[Item.__name__]['add'])
        self.basic_group.permissions.add(perms[Item.__name__]['change'])
        self.basic_group.permissions.add(perms[Item.__name__]['delete'])

        self.basic_user1, created = User.objects.get_or_create(
            username='basic_user1', first_name='Basic1', last_name='User')
        self.basic_user2, created = User.objects.get_or_create(
            username='basic_user2', first_name='Basic2', last_name='User')

        self.basic_user1.groups.add(self.basic_group)
        self.basic_user2.groups.add(self.basic_group)
