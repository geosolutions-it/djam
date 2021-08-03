from django.urls import reverse
from apps.privilege_manager.models import Group
from django.contrib.auth import get_user_model
from apps.billing.utils import SubscriptionManager
from rest_framework.test import APIClient
from django.test import TestCase



class ApiKeyManagerTest(TestCase):
    def setUp(self):
        self.user, _ = get_user_model().objects.get_or_create(username='admin', password="admin", is_superuser=True)
        self.client = APIClient()
        self.sub_manager = SubscriptionManager()
        self.free_group = Group.objects.get(name='free')
        self.pro_group = Group.objects.get(name='pro')
        self.enterprise_group = Group.objects.get(name='enterprise')

    def test_user_with_enterprise_sub(self):
        """
        User with ONLY enteprise subscription can create API token
        """
        self.sub_manager.create_company_subscription(self.enterprise_group, self.user)
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(reverse('api_key_manager'))
        self.assertEqual(200, resp.status_code)
        self.assertTrue(resp.json().get('created'))

    def test_user_with_free_sub(self):
        """
        User with ONLY free subscription cannot create API token
        """
        self.sub_manager.create_individual_subscription(self.free_group, self.user)
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(reverse('api_key_manager'))
        self.assertEqual(403, resp.status_code)

    def test_user_with_pro_sub(self):
        """
        User with ONLY pro subscription cannot create API token
        """
        self.sub_manager.create_individual_subscription(self.pro_group, self.user)
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(reverse('api_key_manager'))
        self.assertEqual(403, resp.status_code)

    def test_user_with_enterprise_and_free_sub(self):
        """
        User with enteprise subscription and free subscription can create API token
        """
        self.sub_manager.create_individual_subscription(self.free_group, self.user)
        self.sub_manager.create_company_subscription(self.enterprise_group, self.user)
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(reverse('api_key_manager'))
        self.assertEqual(200, resp.status_code)
        self.assertTrue(resp.json().get('created'))

    def test_user_with_enterprise_pro_sub(self):
        """
        User with enteprise subscription and free subscription can create API token
        """
        self.sub_manager.create_individual_subscription(self.pro_group, self.user)
        self.sub_manager.create_company_subscription(self.enterprise_group, self.user)
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(reverse('api_key_manager'))
        self.assertEqual(200, resp.status_code)
        self.assertTrue(resp.json().get('created'))
