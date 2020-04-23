from django import forms
from django.core import exceptions
from django.shortcuts import reverse
from django.test import TestCase, Client

from tests.factories.user_management_factory import UserFactory
from apps.user_management.forms import UMAuthenticationForm


class TestUserManagement(TestCase):

    def test_login_email_not_confirmed(self):
        user_psw = 'some_password'
        user = UserFactory(email_confirmed=False)
        user.set_password(user_psw)
        user.save()

        form = UMAuthenticationForm(None, {
            'username': user.username,
            'password': user_psw,
        })

        self.assertFalse(form.is_valid(), "Email not confirmed login: authentication form is valid.")
        with self.assertRaises(forms.ValidationError) as validation_error:
            form.clean()

        self.assertEqual(
            validation_error.exception.code,
            'email_not_confirmed',
            f"Email not confirmed login: authentication form raised forms.ValidationError with '{validation_error.exception.code}'"
            f" instead of'email_not_confirmed' code."
        )

    def test_login_with_username(self):
        web_client = Client()

        user_psw = 'some_password'
        user_username = 'user'
        user = UserFactory(username=user_username)
        user.set_password(user_psw)
        user.save()

        authentication_response = web_client.post(reverse('login'), {'username': user_username, 'password': user_psw})

        self.assertFalse(authentication_response.wsgi_request.user.is_anonymous, "Username authentication returned anonymous user")

    def test_login_with_email(self):
        web_client = Client()

        user_psw = 'some_password'
        user = UserFactory()
        user.set_password(user_psw)
        user.save()

        authentication_response = web_client.post(reverse('login'), {'username': user.email, 'password': user_psw})

        self.assertFalse(authentication_response.wsgi_request.user.is_anonymous, "Email authentication returned anonymous user")

    def test_login_case_insensitive_email(self):
        web_client = Client()

        user_psw = 'some_password'
        user = UserFactory()
        user.set_password(user_psw)
        user.save()

        authentication_response = web_client.post(reverse('login'), {'username': user.email.capitalize(), 'password': user_psw})

        self.assertFalse(authentication_response.wsgi_request.user.is_anonymous, "Email case insensitive authentication returned anonymous user")

    def test_user_page_authenticated_access(self):
        web_client = Client()
        user = UserFactory()

        web_client.force_login(user)
        account_page_response = web_client.get(reverse('user_account', kwargs={'id': user.id}))

        self.assertEqual(account_page_response.status_code, 200, "User's account page: Response status code is not 200.")

    def test_user_page_unauthenticated_access(self):
        web_client = Client()
        user = UserFactory()

        account_page_response = web_client.get(reverse('user_account', kwargs={'id': user.id}))

        self.assertEqual(account_page_response.status_code, 302, "User's account page: Response status code is not 302.")
        self.assertTrue(
            reverse('login') in account_page_response['Location'],
            f"User's account page: Redirection pointed at {account_page_response['Location']} instead of the login page."
        )

    def test_user_page_of_different_user_access(self):
        web_client = Client()
        user_1 = UserFactory()
        user_2 = UserFactory()

        # login user_1
        web_client.force_login(user_1)
        # try to acces user_2's account page as user_2
        account_page_response = web_client.get(reverse('user_account', kwargs={'id': user_2.id}))
        self.assertEqual(account_page_response.status_code, 403, "Another user's account page: Response status code is not 403.")

        print(account_page_response)
