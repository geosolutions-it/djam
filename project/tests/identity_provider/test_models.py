from unittest.mock import patch

from django.core.exceptions import MultipleObjectsReturned
from django.test import TestCase

from apps.identity_provider.models import ApiKey
from tests import UserFactory, ApiKeyFactory
from django.db import models


class ApiKeyTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ApiKeyTest, cls).setUpClass()
        cls.user = UserFactory()

    def test_update(self):
        a = ApiKeyFactory(user=self.user)
        a.revoked = True
        a.save()

        self.assertTrue(ApiKey.objects.get(user=self.user).revoked)

    def test_user_api_key_management(self):
        initial_api_keys = 0
        a = ApiKey.objects.create(user=self.user)
        self.assertEqual(
            ApiKey.objects.filter(user=self.user).count(), initial_api_keys + 1
        )

        # create another key. user has valid one
        a = ApiKey.objects.create(user=self.user)
        self.assertEqual(
            ApiKey.objects.filter(user=self.user).count(), initial_api_keys + 2
        )
        self.assertNotEqual(ApiKey.objects.filter(user=self.user).first(), a)

        # revoke key and recreate new one
        a.revoked = True
        a.save()

        a = ApiKey.objects.create(user=self.user)
        self.assertEqual(
            ApiKey.objects.filter(user=self.user).count(), initial_api_keys + 3
        )
