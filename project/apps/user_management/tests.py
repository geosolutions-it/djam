from django.test import TestCase
import copy

# Create your tests here.
from apps.user_management.models import User, UserActivationCode


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
        self.assertEquals(
            1,
            UserActivationCode.objects.filter(user=u).count()
        )

class UserPreSaveActivationEmail(TestCase):
    def test_user_activation_pre_hook(self):
        # TODO - This pre hook may need 
        # refactoring and something like DI
        # so we can mock and test
        pass