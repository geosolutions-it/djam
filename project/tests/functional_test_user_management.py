from django import forms
from django.contrib.auth import get_user_model
from django.core import exceptions
from django.shortcuts import reverse
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APITestCase
from apps.billing.models import Company
from apps.administration.models import IndividualSubscription

from tests.factories.user_management_factory import UserFactory, GroupFactory
from apps.user_management.forms import UMAuthenticationForm
from apps.billing.utils import subscription_manager


class TestUserManagement(TestCase):
    def test_login_email_not_confirmed(self):
        user_psw = "some_password"
        user = UserFactory(email_confirmed=False)
        user.set_password(user_psw)
        user.save()

        form = UMAuthenticationForm(
            None, {"username": user.username, "password": user_psw, }
        )

        self.assertFalse(
            form.is_valid(), "Email not confirmed login: authentication form is valid."
        )
        with self.assertRaises(forms.ValidationError) as validation_error:
            form.clean()

        self.assertEqual(
            validation_error.exception.code,
            "email_not_confirmed",
            f"Email not confirmed login: authentication form raised forms.ValidationError with '{validation_error.exception.code}'"
            f" instead of'email_not_confirmed' code.",
        )

    def test_login_with_username(self):
        web_client = Client()

        user_psw = "some_password"
        user_username = "user"
        user = UserFactory(username=user_username)
        user.set_password(user_psw)
        user.save()

        web_client.force_login(user)
        authentication_response = web_client.post(reverse("login"))

        self.assertFalse(
            authentication_response.wsgi_request.user.is_anonymous,
            "Username authentication returned anonymous user",
        )

    def test_login_with_email(self):
        web_client = Client()

        user_psw = "some_password"
        user = UserFactory()
        user.set_password(user_psw)
        user.save()

        authentication_response = web_client.post(
            reverse("login"), {"username": user.email, "password": user_psw}
        )

        self.assertFalse(
            authentication_response.wsgi_request.user.is_anonymous,
            "Email authentication returned anonymous user",
        )

    def test_login_case_insensitive_email(self):
        web_client = Client()

        user_psw = "some_password"
        user = UserFactory()
        user.set_password(user_psw)
        user.save()

        authentication_response = web_client.post(
            reverse("login"),
            {"username": user.email.capitalize(), "password": user_psw},
        )

        self.assertFalse(
            authentication_response.wsgi_request.user.is_anonymous,
            "Email case insensitive authentication returned anonymous user",
        )

    def test_user_page_authenticated_access(self):
        web_client = Client()
        user = UserFactory()

        web_client.force_login(user)
        account_page_response = web_client.get(
            reverse("user_account", kwargs={"id": user.id})
        )

        self.assertEqual(
            account_page_response.status_code,
            200,
            "User's account page: Response status code is not 200.",
        )

    def test_user_page_unauthenticated_access(self):
        web_client = Client()
        user = UserFactory()

        account_page_response = web_client.get(
            reverse("user_account", kwargs={"id": user.id})
        )

        self.assertEqual(
            account_page_response.status_code,
            302,
            "User's account page: Response status code is not 302.",
        )
        self.assertTrue(
            reverse("login") in account_page_response["Location"],
            f"User's account page: Redirection pointed at {account_page_response['Location']} instead of the login page.",
        )

    def test_user_page_of_different_user_access(self):
        web_client = Client()
        user_1 = UserFactory()
        user_2 = UserFactory()

        # login user_1
        web_client.force_login(user_1)
        # try to acces user_2's account page as user_2
        account_page_response = web_client.get(
            reverse("user_account", kwargs={"id": user_2.id})
        )
        self.assertEqual(
            account_page_response.status_code,
            403,
            "Another user's account page: Response status code is not 403.",
        )

        print(account_page_response)


class TestGetUserData(APITestCase):

    def setUp(self):
        self.admin = UserFactory(username='admin', is_staff=True, is_superuser=True)
        self.user = UserFactory(username='test_user')
        self.u1 = UserFactory(username='u1', last_login='2020-05-21T07:59:26.324Z')
        self.u2 = UserFactory(username='u2', last_login='2020-05-11T07:59:26.342Z')   
        self.pro_group = GroupFactory(name='pro')
        self.ent_group = GroupFactory(name='enterprise')
        self.free_group = GroupFactory(name='free')        
        #self.free_group.users.add(*[self.user, self.u1, self.u2, self.admin])
        #self.pro_group.users.add(self.admin)
        #self.ent_group.users.add(self.u1)
        User = get_user_model()
        self.admin = User.objects.get(username='admin')
        self.user = User.objects.get(username='test_user')

    def test_user_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('fetch_users-list'))
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_allowed(self):
        users_count = 4
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse('fetch_users-list'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get('count', 0), users_count)

    def test_user_allowed_filter_groups(self):
        IndividualSubscription.objects.filter(user=self.u1).update(groups=self.pro_group)
        users_count = 1
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse('fetch_users-list') + '?groups=pro')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get('count', 0), users_count)

    def test_user_allowed_filter_wrong_groups(self):
        users_count = 0
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse('fetch_users-list') + '?groups=test')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get('count', 0), users_count)

    def test_user_allowed_filter_mult_groups(self):
        company, _ = Company.objects.get_or_create(company_name='Foo')
        company.users.add(self.admin)
        subscription_manager.create_company_subscription(
            groups=self.ent_group,
            company=company
        )   
        IndividualSubscription.objects.filter(user=self.u1).update(groups=self.pro_group)
        users_count = 2
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse('fetch_users-list') + '?groups=enterprise,pro')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get('count', 0), users_count)

    def test_user_allowed_filter_wrong_filter(self):
        users_count = 4
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse('fetch_users-list') + '?not_a_filter=free,pro')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get('count', 0), users_count)

    def test_user_allowed_filter_older_than(self):
        users_count = 2
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse('fetch_users-list') + '?older=2020-05-21T11:19:10Z')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get('count', 0), users_count)

    def test_user_allowed_filter_newer_than(self):
        users_count = 0
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse('fetch_users-list') + '?newer=2020-05-21T11:19:10Z')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get('count', 0), users_count)

    def test_user_allowed_filter_wrong_date(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse('fetch_users-list') + '?newer=wrongg_fate')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
