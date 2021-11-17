from apps.privilege_manager.models import Group
from apps.billing.utils import subscription_manager
from django.test import TestCase
from apps.user_management.models import User, UserActivationCode
from apps.billing.models import Company
from apps.administration.models import IndividualSubscription


def create_user(username="test_user", email="johnsmith@example.net", **kwargs):
    return User.objects.create(username=username, email=email, **kwargs)


class UserTests(TestCase):
    def test_user_creation(self):
        u = create_user()
        self.assertTrue(isinstance(u, User))

    def test_names(self):
        first_name = "John"
        last_name = "Smith"
        u = create_user(first_name=first_name, last_name=last_name)
        self.assertEquals(u.get_full_name(), first_name + " " + last_name)
        self.assertEquals(u.get_short_name(), first_name)

    def test_cleaning(self):
        u = create_user(email="johnsmith@EXAMPLE.net")
        u.clean()
        self.assertEquals(u.email, "johnsmith@example.net")
        self.assertEquals(u.email, u.username)


class UserActivationCodeTests(TestCase):
    def create_user_activation(self):
        u = create_user(email="johnsmith@example.net")
        ua = UserActivationCode(user=u)

        return ua

    def test_user_activation_regeneration(self):
        ua_original = self.create_user_activation()
        ua_code = ua_original.activation_code
        ua_date = ua_original.creation_date
        ua_original.regenerate_code()

        self.assertNotEquals(ua_original.activation_code, ua_code)
        self.assertNotEquals(ua_original.creation_date, ua_date)


class UserPostSaveActivationCode(TestCase):
    def test_user_activation_post_hook(self):
        u = create_user(email="johnsmith@example.net")
        self.assertEquals(1, UserActivationCode.objects.filter(user=u).count())


class UserPreSaveActivationEmail(TestCase):
    def test_user_activation_pre_hook(self):
        # TODO - This pre hook may need
        # refactoring and something like DI
        # so we can mock and test
        pass

class UsersGroup(TestCase):
    def setUp(self):
        self.user = create_user(email_confirmed=True)
        self.sub_manager = subscription_manager
        self.free_group = Group.objects.get(name='free')
        self.pro_group = Group.objects.get(name='pro')
        self.enterprise_group = Group.objects.get(name='enterprise')
        self.company, _ = Company.objects.get_or_create(company_name='Foo')
        self.company.users.add(self.user)

    def test_get_highest_user_sub_free(self):
        """
        User with only free subscription will return FREE as group perm
        """
        self.assertEqual('free', self.user.get_group())

    def test_get_highest_user_sub_pro(self):
        """
        User with only free subscription will return FREE as group perm
        """
        IndividualSubscription.objects.filter(user=self.user).update(groups=self.pro_group)
        self.assertEqual('pro', self.user.get_group())

    def test_get_highest_user_sub_free_with_company_sub(self):
        """
        User with only free subscription and an Enterprise subscription will return ENTERPRISE as group perm
        """
        self.sub_manager.create_company_subscription(self.enterprise_group, self.company)
        self.assertEqual('enterprise', self.user.get_group())

    def test_get_highest_user_sub_pro_with_company_sub(self):
        """
        User with only free subscription and an Enterprise subscription will return ENTERPRISE as group perm
        """
        self.sub_manager.create_company_subscription(self.enterprise_group, self.company)
        IndividualSubscription.objects.filter(user=self.user).update(groups=self.pro_group)
        self.assertEqual('enterprise', self.user.get_group())

    def test_get_highest_user_sub_enterprise_sub(self):
        """
        User with only free subscription and an Enterprise subscription will return ENTERPRISE as group perm
        """
        self.sub_manager.create_company_subscription(self.enterprise_group, self.company)
        self.assertEqual('enterprise', self.user.get_group())
