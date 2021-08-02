from apps.billing.utils import SubscriptionException, SubscriptionManager
from apps.privilege_manager.models import Group
from django.test import TestCase

# Create your tests here.

class SubscriptionManagerTest(TestCase):
    def setUp(self):
        self.sut = SubscriptionManager()
        self.free_group = Group.objects.get(name='free')
        self.pro_group = Group.objects.get(name='pro')
        self.enterprise_group = Group.objects.get(name='enterprise')

    def test_indivitual_sub_free_group(self):
        """
        Given FREE group CAN create an INDIVIDUAL sub
        """
        subscription = self.sut.create_individual_subscription(
            groups=self.free_group
        )
        self.assertIsNotNone(subscription)

    def test_indivitual_sub_pro_group(self):
        """
        Given PRO group CAN create an INDIVIDUAL sub
        """
        subscription = self.sut.create_individual_subscription(groups=self.pro_group)
        self.assertIsNotNone(subscription)

    def test_indivitual_sub_enterprise_group(self):
        """
        Given ENTERPRISE group CANNOT create an INDIVIDUAL sub
        """
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_individual_subscription(groups=self.enterprise_group)

    def test_company_sub_enterprise_group(self):
        """
        Given ENTERPRISE group CAN create a COMPANY sub
        """
        subscription = self.sut.create_company_subscription(groups=self.enterprise_group)
        self.assertIsNotNone(subscription)

    def test_company_sub_free_group(self):
        """
        Given FREE group CANNOT create an COMPANY sub
        """
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_company_subscription(groups=self.free_group)

    def test_company_sub_pro_group(self):
        """
        Given PRO group CANNOT create an COMPANY sub
        """
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_company_subscription(groups=self.pro_group)

    def test_user1_no_subs(self):
        """
        user1 with 0 individual active sub and 0 company active sub -> Valid"""
        pass

    def test_user1_only_1_active_individual_sub(self):
        """
        user1 with 1 individual active sub and 0 company active sub -> Valid"""
        pass

    def test_user1_only_1_active_company_sub(self):
        """
        user1 with 0 individual active sub and 1 company active sub -> Valid"""
        pass

    def test_user1_with_active_1_individual_1_company_sub(self):
        """
        user1 with 1 individual active sub and 1 company active sub -> Valid"""
        pass

    def test_user1_with_active_1_inactive_individual_1_active_company(self):
        """
        user1 with 10 individual inactive sub and 1 company active sub -> Valid"""
        pass

    def test_user1_with_active_0_individual_1_inactive_active_company(self):
        """
        user1 with 0 individual active sub and 10 company inactive sub -> Valid"""
        pass

    def test_user1_with_1_inactive_individual_and_1_inactive_company_sub(self):
        """
        user1 with 0 individual inactive sub and 0 company inactive sub -> Valid"""
        pass

    def test_user1_with_2_active_individual_and_0_company(self):
        """
        user1 with 2 individual active sub and 0 company active sub -> Invalid"""
        pass

    def test_user1_with_2_active_individual_and_1_active_company(self):
        """
        user1 with 2 individual active sub and 1 company active sub -> Invalid"""
        pass

    def test_user1_0_active_individual_company_and_2_active_company_sub(self):
        """
        user1 with 0 individual active sub and 2 company active sub -> Invalid"""
        pass

    def test_user1_with_1_inactive_individual_and_2_active_company_sub(self):
        """
        user1 with 1 individual inactive sub and 2 company active sub -> Invalid"""
        pass