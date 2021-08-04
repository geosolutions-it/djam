from datetime import timedelta
from django.utils import timezone
from apps.billing.utils import SubscriptionException, SubscriptionManager
from apps.privilege_manager.models import Group
from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

class SubscriptionManagerTest(TestCase):
    def setUp(self):
        self.sut = SubscriptionManager()
        self.free_group = Group.objects.get(name='free')
        self.pro_group = Group.objects.get(name='pro')
        self.enterprise_group = Group.objects.get(name='enterprise')
        self.user, _ = get_user_model().objects.get_or_create(username='admin')

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

    def test_user1_with_2_active_individual_and_0_company(self):
        """
        User1 cannot create new individual subscription if already have one -> InValid
        """

        sub = self.sut.create_individual_subscription(
            groups=self.free_group,
            users=self.user
        )
        # Trying to create a second individual subscription
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_individual_subscription(groups=self.free_group, users=self.user)

    def test_user1_with_1_active_individual_and_1_company(self):
        """
        User1 cannot create new individual subscription if already have one and have company subscription -> InValid
        """

        sub = self.sut.create_individual_subscription(
            groups=self.free_group,
            users=self.user
        )
        sub2 = self.sut.create_company_subscription(
            groups=self.enterprise_group,
            users=self.user
        )
        # Trying to create a second individual subscription
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_individual_subscription(groups=self.free_group, users=self.user)

    def test_user1_no_subs(self):
        """
        user1 with 0 individual active sub and 0 company active sub -> Valid
        """
        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    def test_user1_only_1_active_individual_sub(self):
        """
        user1 with 1 individual active sub and 0 company active sub -> Valid
        """
        subs = self.sut.create_individual_subscription(groups=self.free_group)
        subs.users.add(self.user)
        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    def test_user1_only_1_active_individual_sub_and_add_another(self):
        """
        user1 with 1 individual active sub and 0 company active sub cannot add a new individual sub
        """
        subs = self.sut.create_individual_subscription(groups=self.free_group)
        subs.users.add(self.user)
        with self.assertRaises(SubscriptionException):
            self.sut.can_add_new_subscription_by_user(self.user, sub_type="INDIVIDUAL")

    def test_user1_only_1_active_company_sub(self):
        """
        user1 with 0 individual active sub and 1 company active sub -> Valid
        """
        subs = self.sut.create_company_subscription(groups=self.enterprise_group)
        subs.users.add(self.user)
        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    def test_user1_with_active_1_individual_1_company_sub(self):
        """
        user1 with 1 individual active sub and 1 company active sub -> Valid
        If we the user already have 1 individual and 1 company, we cannot add new subscriptions
        """
        subs = self.sut.create_company_subscription(groups=self.enterprise_group)
        subs2 = self.sut.create_individual_subscription(groups=self.pro_group)
        subs.users.add(self.user)
        subs2.users.add(self.user)
        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertFalse(active_subs)

    def test_user1_with_active_1_inactive_individual_1_active_company(self):
        """
        user1 with 10 individual inactive sub and 1 company active sub -> Valid
        """
        
        subs = self.sut.create_company_subscription(groups=self.enterprise_group)
        # Let 2 individual subs be no longer active
        subs2 = self.sut.create_individual_subscription(
            groups=self.pro_group,
            end_timestamp=timezone.now() -timedelta(days=10)
        )
        subs3 = self.sut.create_individual_subscription(
            groups=self.pro_group,
            end_timestamp=timezone.now() -timedelta(days=10)
        )

        subs.users.add(self.user)
        subs2.users.add(self.user)
        subs3.users.add(self.user)

        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    def test_user1_with_active_0_individual_1_inactive_active_company(self):
        """
        user1 with 0 individual active sub and 10 company inactive sub -> Valid
        """
        subs = self.sut.create_company_subscription(
            groups=self.enterprise_group,
            end_timestamp=timezone.now() -timedelta(days=10)
        )
        subs2 = self.sut.create_company_subscription(
            groups=self.enterprise_group,
            end_timestamp=timezone.now() -timedelta(days=10)
        )
 
        subs.users.add(self.user)
        subs2.users.add(self.user)

        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    def test_user1_with_1_inactive_individual_and_1_inactive_company_sub(self):
        """
        user1 with 0 individual inactive sub and 0 company inactive sub -> Valid
        """
        subs = self.sut.create_company_subscription(
            groups=self.enterprise_group,
            end_timestamp=timezone.now() -timedelta(days=10)
        )
        subs2 = self.sut.create_individual_subscription(
            groups=self.free_group,
            end_timestamp=timezone.now() -timedelta(days=10)
        )
 
        subs.users.add(self.user)
        subs2.users.add(self.user)

        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)
