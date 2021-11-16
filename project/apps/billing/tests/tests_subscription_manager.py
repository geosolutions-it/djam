from datetime import timedelta
from unittest import skip
from apps.administration.models import IndividualSubscription
from apps.billing.models import Company, Subscription
from django.utils import timezone
from apps.billing.utils import SubscriptionException, subscription_manager
from apps.privilege_manager.models import Group
from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

class SubscriptionManagerTest(TestCase):
    def setUp(self):
        self.sut = subscription_manager
        self.free_group = Group.objects.get(name='free')
        self.pro_group = Group.objects.get(name='pro')
        self.enterprise_group = Group.objects.get(name='enterprise')
        self.user, _ = get_user_model().objects.get_or_create(username='admin', email_confirmed=True)
        self.company, _ = Company.objects.get_or_create(company_name='Foo')
        self.company.users.add(self.user)

    def _delete_subs(self):
        s = Subscription.objects.all()
        for x in s:
            x.delete()


    def tearDown(self):
        self._delete_subs()
        
    def test_indivitual_sub_free_group(self):
        """
        Given FREE group CAN create an INDIVIDUAL sub
        """
        # we must delete the previous sub since is created by default when the user is created
        self._delete_subs()

        subscription = self.sut.create_individual_subscription(
            groups=self.free_group,
            users=self.user
        )
        self.assertIsNotNone(subscription)

    def test_indivitual_sub_pro_group(self):
        """
        Given PRO group CAN create an INDIVIDUAL sub
        """
        self._delete_subs()
        subscription = self.sut.create_individual_subscription(groups=self.pro_group, users=self.user)
        self.assertIsNotNone(subscription)

    def test_indivitual_sub_enterprise_group(self):
        """
        Given ENTERPRISE group CANNOT create an INDIVIDUAL sub
        """
        self._delete_subs()
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_individual_subscription(groups=self.enterprise_group, users=self.user)

    def test_company_sub_enterprise_group(self):
        """
        Given ENTERPRISE group CAN create a COMPANY sub
        """
        subscription = self.sut.create_company_subscription(groups=self.enterprise_group, company=self.company)
        self.assertIsNotNone(subscription)

    def test_company_sub_free_group(self):
        """
        Given FREE group CANNOT create an COMPANY sub
        """
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_company_subscription(groups=self.free_group, company=self.company)

    def test_company_sub_pro_group(self):
        """
        Given PRO group CANNOT create an COMPANY sub
        """
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_company_subscription(groups=self.pro_group, company=self.company)

    def test_user1_with_2_active_individual_and_0_company(self):
        """
        User1 cannot create new individual subscription if already have one -> InValid
        """

        # Trying to create a second individual subscription
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_individual_subscription(groups=self.free_group, users=self.user)

    def test_user1_with_1_active_individual_and_1_company(self):
        """
        User1 cannot create new individual subscription if already have one and have company subscription -> InValid
        """
        # the free one is created by default when the user is created
        sub2 = self.sut.create_company_subscription(
            groups=self.enterprise_group,
            company=self.company
        )
        # Trying to create a second individual subscription
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_individual_subscription(groups=self.free_group, users=self.user)

    def test_user1_no_subs(self):
        """
        user1 with 0 individual active sub and 0 company active sub -> Valid
        """
        self._delete_subs()
        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    def test_user1_only_1_active_individual_sub(self):
        """
        user1 with 1 individual active sub and 0 company active sub -> Valid
        """
        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    def test_user1_only_1_active_individual_sub_and_add_another(self):
        """
        user1 with 1 individual active sub and 0 company active sub cannot add a new individual sub
        """
        with self.assertRaises(SubscriptionException):
            self.sut.can_add_new_subscription_by_user(self.user, sub_type="INDIVIDUAL")

    def test_user1_only_1_active_company_sub(self):
        """
        user1 with 0 individual active sub and 1 company active sub -> Valid
        """
        self._delete_subs()
        subs = self.sut.create_company_subscription(groups=self.enterprise_group, company=self.company)
        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    def test_user1_with_active_1_individual_1_company_sub(self):
        """
        user1 with 1 individual active sub and 1 company active sub -> Valid
        If we the user already have 1 individual and 1 company, we cannot add new subscriptions
        """
        subs = self.sut.create_company_subscription(groups=self.enterprise_group, company=self.company)
        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertFalse(active_subs)

    def test_user1_with_active_1_inactive_individual_1_active_company(self):
        """
        user1 with 1 individual inactive sub and 1 company active sub -> Valid
        """
        
        self.sut.create_company_subscription(groups=self.enterprise_group, company=self.company)
        s = IndividualSubscription.objects.filter(user=self.user)
        s.update(end_timestamp=timezone.now() -timedelta(days=10))

        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    def test_user1_with_active_0_individual_1_inactive_active_company(self):
        """
        user1 with 0 individual active sub and 10 company inactive sub -> Valid
        """
        subs = self.sut.create_company_subscription(
            groups=self.enterprise_group,
            company=self.company,
            end_timestamp=timezone.now() -timedelta(days=10)
        )

        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    def test_user1_with_1_inactive_individual_and_1_inactive_company_sub(self):
        """
        user1 with 0 individual inactive sub and 0 company inactive sub -> Valid
        """
        subs = self.sut.create_company_subscription(
            groups=self.enterprise_group,
            company=self.company,
            end_timestamp=timezone.now() -timedelta(days=10)
        )
 
        active_subs = self.sut.can_add_new_subscription_by_user(self.user)
        self.assertTrue(active_subs)

    @skip
    def test_subscription_update(self):
        """
        A Subscription can be updated
        """
        subs = self.sut.create_company_subscription(
            groups=self.enterprise_group,
            company=self.company,
            end_timestamp=timezone.now() -timedelta(days=10)
        )
        
        self.sut.update_subscription(subs, company_name='New Fantastic Company')
        subs.refresh_from_db()

        self.assertEqual('New Fantastic Company', subs.company_name)

