# -*- coding: utf-8 -*-
# Django
from django.db.utils import IntegrityError
from django.test import TestCase

# External
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Local
from .models import Checklist, Item
from django_checklist.common.models import Tag
from django_checklist.django_auth.mixins import PermissionsTestCaseMixin

############
# Checklist
############

class ChecklistCreationTestCase(TestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        self.user1 = None

        self.title1 = None
        self.title2 = ''
        self.title3 = 'New Checklist'
        self.title4 = 'リスト'
        self.title5 = 'a' * 30

    #######
    # user
    #######

    def test_none_user(self):
        with self.assertRaises(ValueError):
            checklist = Checklist.objects.create(user=self.user1, 
                title=self.title3)

    def test_valid_user(self):
        checklist = Checklist.objects.create(user=self.basic_user1, 
            title=self.title3)
        self.assertEqual(checklist.user, self.basic_user1)

    ########
    # title
    ########

    def test_none_title(self):
        with self.assertRaises(IntegrityError):
            checklist = Checklist.objects.create(user=self.basic_user1, 
                title=self.title1)

    def test_blank_title(self):
        checklist = Checklist.objects.create(user=self.basic_user1, 
            title=self.title2)

    def test_valid_ascii_title(self):
        checklist = Checklist.objects.create(user=self.basic_user1, 
            title=self.title3)
        self.assertEqual(checklist.title, self.title3)

    def test_unicode_title(self):
        checklist = Checklist.objects.create(user=self.basic_user1, 
            title=self.title4)
        self.assertEqual(checklist.title, self.title4)

    def test_max_length_title(self):
        checklist = Checklist.objects.create(user=self.basic_user1, 
            title=self.title5)
        self.assertEqual(checklist.title, self.title5)

class ChecklistAPIListTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        self.url = reverse('checklist-list')

    def test_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ChecklistAPICreateTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        self.url = reverse('checklist-list')
        self.data = {'title': 'Shopping'}

    def test_unauthenticated(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ChecklistAPIUpdateTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        checklist, created = Checklist.objects.get_or_create(
            user=self.basic_user1, title='Shopping')
        self.url = reverse('checklist-detail', args=(checklist.id,))

        self.data = {'title': 'Not Shopping'}

    def test_unauthenticated(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nonowner_user(self):
        self.client.force_authenticate(user=self.basic_user2)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ChecklistAPIDeleteTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        checklist, created = Checklist.objects.get_or_create(
            user=self.basic_user1, title='Shopping')
        self.url = reverse('checklist-detail', args=(checklist.id,))

    def test_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_nonowner_user(self):
        self.client.force_authenticate(user=self.basic_user2)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ChecklistAPIDetailTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        checklist, created = Checklist.objects.get_or_create(
            user=self.basic_user1, title='Shopping')
        self.url = reverse('checklist-detail', args=(checklist.id,))

    def test_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nonowner_user(self):
        self.client.force_authenticate(user=self.basic_user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#######
# Item
#######

class ItemCreationTestCase(TestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        self.checklist1 = None
        self.checklist2, created = Checklist.objects.get_or_create(
            user=self.basic_user1, title='Homework')

        self.description1 = None
        self.description2 = ''
        self.description3 = 'Study French'
        self.description4 = 'アイテム'
        self.description5 = 'a' * 100

    ############
    # checklist
    ############

    def test_none_checklist(self):
        with self.assertRaises(ValueError):
            item = Item.objects.create(checklist=self.checklist1, 
                description=self.description3)

    def test_valid_checklist(self):
        item = Item.objects.create(checklist=self.checklist2, 
            description=self.description3)
        self.assertEqual(item.checklist, self.checklist2)

    ##############
    # description
    ##############

    def test_none_description(self):
        with self.assertRaises(IntegrityError):
            item = Item.objects.create(checklist=self.checklist2, 
                description=self.description1)
    
    def test_blank_description(self):
        item = Item.objects.create(checklist=self.checklist2, 
            description=self.description2)
    
    def test_valid_ascii_description(self):
        item = Item.objects.create(checklist=self.checklist2, 
            description=self.description3)
        self.assertEqual(item.description, self.description3)

    def test_unicode_description(self):
        item = Item.objects.create(checklist=self.checklist2, 
            description=self.description4)
        self.assertEqual(item.description, self.description4)

    def test_max_length_description(self):
        item = Item.objects.create(checklist=self.checklist2, 
            description=self.description5)
        self.assertEqual(item.description, self.description5)

    ##############
    # is_complete
    ##############

    def test_default_is_complete(self):
        item = Item.objects.create(checklist=self.checklist2, 
            description=self.description3)
        self.assertEqual(item.is_complete, False)

class ItemAPICreateTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        checklist, created = Checklist.objects.get_or_create(
            user=self.basic_user1, title='Shopping')
        checklist_url = reverse('checklist-detail', args=(checklist.id,))

        self.url = reverse('item-list')
        self.data = {
            'checklist': checklist_url, 
            'description': 'Milk'
        }

    def test_unauthenticated(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_checklist_nonowner_user(self):
        self.client.force_authenticate(user=self.basic_user2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ItemAPIUpdateTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        checklist, created = Checklist.objects.get_or_create(
            user=self.basic_user1, title='Shopping')
        checklist_url = reverse('checklist-detail', args=(checklist.id,))
        item, created = Item.objects.get_or_create(checklist=checklist, 
            description='Milk')

        self.url = reverse('item-detail', args=(item.id,))
        self.data = {
            'checklist': checklist_url, 
            'description': 'Milk', 
            'is_complete': True
        }

    def test_unauthenticated(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_checklist_nonowner_user(self):
        self.client.force_authenticate(user=self.basic_user2)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ItemAPIDeleteTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        checklist, created = Checklist.objects.get_or_create(
            user=self.basic_user1, title='Shopping')
        checklist_url = reverse('checklist-detail', args=(checklist.id,))
        item, created = Item.objects.get_or_create(checklist=checklist, 
            description='Milk')

        self.url = reverse('item-detail', args=(item.id,))

    def test_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_checklist_nonowner_user(self):
        self.client.force_authenticate(user=self.basic_user2)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
