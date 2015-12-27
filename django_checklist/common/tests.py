# -*- coding: utf-8 -*-
# Django
from django.db.utils import IntegrityError
from django.test import TestCase

# External
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Local
from .models import Tag
from django_checklist.django_auth.mixins import PermissionsTestCaseMixin

class TagCreationTestCase(TestCase):
    def setUp(self):
        self.name1 = None
        self.name2 = ''
        self.name3 = 'sports'
        self.name4 = 'デモ'

    def test_none_name(self):
        with self.assertRaises(IntegrityError):
            tag = Tag.objects.create(name=self.name1)

    def test_blank_name(self):
        tag = Tag.objects.create(name=self.name2)
        self.assertEqual(tag.name, self.name2)

    def test_valid_ascii_name(self):
        tag = Tag.objects.create(name=self.name3)
        self.assertEqual(tag.name, self.name3)

    def test_unicode_name(self):
        tag = Tag.objects.create(name=self.name4)
        self.assertEqual(tag.name, self.name4)

class TagAPIListTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        self.url = reverse('tag-list')

    def test_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TagAPICreateTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        self.url = reverse('tag-list')
        self.data = {'name': 'swing'}

    def test_unauthenticated(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TagAPIUpdateTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        tag, created = Tag.objects.get_or_create(name='usa')
        self.url = reverse('tag-detail', args=(tag.id,))

        self.data = {'name': 'china'}

    def test_unauthenticated(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TagAPIDeleteTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        tag, created = Tag.objects.get_or_create(name='usa')
        self.url = reverse('tag-detail', args=(tag.id,))
    
    def test_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TagAPIDetailTestCase(APITestCase, PermissionsTestCaseMixin):
    def setUp(self):
        self.initialize()
        tag, created = Tag.objects.get_or_create(name='usa')
        self.url = reverse('tag-detail', args=(tag.id,))

    def test_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated(self):
        self.client.force_authenticate(user=self.basic_user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
