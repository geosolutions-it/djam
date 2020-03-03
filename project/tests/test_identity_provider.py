import re
from unittest import skip

from django.test import TestCase, Client
from django.core.management import call_command
from django.shortcuts import reverse
from oidc_provider import models as oidc_models

from apps.identity_provider import models
from apps.privilege_manager.models import Group

from tests.factories.identity_provider_factory import OIDCConfidentialClientFactory, ApiKeyFactory
from tests.factories.user_management_factory import UserFactory


class IdentityProviderBaseTestCase(TestCase):

    # Note: oidc_provider returns redirect response of HttpResponse type, so assertRedirects() cannot be used for
    # response validation, as it expects HttpResponseRedirect instance

    @classmethod
    def setUpTestData(cls):
        call_command('creatersakey')
        cls.oidc_client = OIDCConfidentialClientFactory.create(response_types=[oidc_models.ResponseType.objects.get(value='code')])
        cls.oidc_client_redirect_uri = cls.oidc_client.redirect_uris[0]

    def oidc_authorize(self, web_client: Client, view_name: str = 'authorize'):
        """
        Method performing OIDC authorization of a logged in user.

        :return: Djam HttpResponse
        """
        return web_client.get(
            reverse(view_name),
            {
                'response_type': 'code',
                'client_id': self.oidc_client.client_id,
                'redirect_uri': self.oidc_client_redirect_uri,
                'scope': 'openid profile email user_id',
            },
        )

    def oidc_token(self, web_client: Client, oidc_code: str):
        """
        Method performing OIDC code to token exchange.

        :return: Djam HttpResponse
        """
        return web_client.post(
            reverse('token'),
            {
                'grant_type': 'authorization_code',
                'code': oidc_code,
                'redirect_uri': self.oidc_client_redirect_uri,
                'client_id': self.oidc_client.client_id,
                'client_secret': self.oidc_client.client_secret,
            },
        )

    def access_token_intorspect(self, web_client: Client, access_token: str):
        """
        Method performing AuthKey introspection.

        :return: Djam HttpResponse
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        return web_client.post(reverse('geoserver_token_introspect'), **headers)

    def authkey_introspect(self, web_client: Client, session_token: str):
        """
        Method performing AuthKey introspection.

        :return: Djam HttpResponse
        """
        return web_client.get(
            reverse('authkey_introspect'),
            {
                'authkey': session_token,
            },
        )


class TestOpenIdCustomization(IdentityProviderBaseTestCase):

    def test_stateless_authorize_response(self):
        user = UserFactory()
        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        # OIDC authorize
        authorize_response = self.oidc_authorize(web_client, view_name='stateless_authorize')

        self.assertEqual(authorize_response.status_code, 302, "OIDC /authorize didn't return 302 redirection response.")
        self.assertIn('code=', authorize_response['Location'], "OIDC /authorize didn't return a code")
        self.assertNotIn('state=', authorize_response['Location'], "Geoserver OIDC /authorize customization returned empty state parameter")

    def test_authorize_djam_session_update(self):
        user = UserFactory()
        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        # OIDC authorize
        authorize_response = self.oidc_authorize(web_client)

        self.assertEqual(authorize_response.status_code, 302, "OIDC /authorize didn't return 302 redirection response.")
        self.assertIn('code=', authorize_response['Location'], "OIDC /authorize didn't return a code")

        oidc_code = re.search(r"code=(\w+)&?.*$", authorize_response['Location']).groups()[0]
        djam_session = models.Session.objects.filter(oidc_code=oidc_code).first()

        self.assertIsNotNone(djam_session, "OIDC /authorize didn't update the user session with oidc code")

    def test_token_with_session_key(self):
        user = UserFactory()
        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        # OIDC authorize
        authorize_response = self.oidc_authorize(web_client)

        self.assertEqual(authorize_response.status_code, 302, "OIDC /authorize didn't return 302 redirection response.")
        self.assertIn('code=', authorize_response['Location'], "OIDC /authorize didn't return a code")

        # OIDC token exchange
        oidc_code = re.search(r"code=(\w+)&?.*$", authorize_response['Location']).groups()[0]
        token_response = self.oidc_token(web_client, oidc_code)

        self.assertEqual(token_response.status_code, 200, "OIDC /token: response status code is not 200")
        self.assertIn('access_token', token_response.json(), "OIDC /token: access_token not in JSON response")
        self.assertIn('id_token', token_response.json(), "OIDC /token: id_token not in JSON response")
        self.assertIn('session_token', token_response.json(), "OIDC /token: session_token not in JSON response")
        self.assertIsNotNone(token_response.json().get('session_token'), "OIDC /token: session_token in JSON response is None")
        self.assertIn('expires_in', token_response.json(), "OIDC /token: expires_in not in JSON response")

    # @skip("This test should be run only on server with unsecured HTTP")
    def test_require_https_for_geoserver_token_introspection(self):
        user = UserFactory()
        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        # OIDC authorize
        authorize_response = self.oidc_authorize(web_client)

        self.assertEqual(authorize_response.status_code, 302, "OIDC /authorize didn't return 302 redirection response.")
        self.assertIn('code=', authorize_response['Location'], "OIDC /authorize didn't return a code")

        # OIDC token exchange
        oidc_code = re.search(r"code=(\w+)&?.*$", authorize_response['Location']).groups()[0]
        token_response = self.oidc_token(web_client, oidc_code)

        self.assertEqual(token_response.status_code, 200, "OIDC /token: response status code is not 200")
        self.assertIn('access_token', token_response.json(), "OIDC /token: access_token not in JSON response")

        self.access_token_intorspect(web_client, token_response.json().get('access_token'))

        # Introspect access token
        with self.settings(REQUIRE_SECURE_HTTP_FOR_GEOSERVER_INTROSPECTION=True):
            access_token_response = self.access_token_intorspect(web_client, token_response.json().get('access_token'))

        self.assertEqual(access_token_response.status_code, 400, "OIDC token introspection with HTTPS required: response status code is not 400")


class TestAuthKey(IdentityProviderBaseTestCase):

    def openid_login(self, web_client: Client, user: UserFactory) -> str:
        """
        Method performing OIDC login and returning session_token from token exchange flow.

        :return: session_token
        """
        # force web client's login
        web_client.force_login(user)

        # OIDC authorize
        authorize_response = self.oidc_authorize(web_client)

        self.assertEqual(authorize_response.status_code, 302, "OIDC /authorize didn't return 302 redirection response.")
        self.assertIn('code=', authorize_response['Location'], "OIDC /authorize didn't return a code")

        # OIDC token exchange
        oidc_code = re.search(r"code=(\w+)&?.*$", authorize_response['Location']).groups()[0]
        token_response = self.oidc_token(web_client, oidc_code)

        self.assertEqual(token_response.status_code, 200, "OIDC /token: response status code is not 200")
        self.assertIn('session_token', token_response.json(), "OIDC /token: session_token not in JSON response")
        self.assertIsNotNone(token_response.json().get('session_token'), "OIDC /token: session_token in JSON response is None")

        return token_response.json().get('session_token')

    def test_validate_valid_session_key(self):
        web_client = Client()
        user = UserFactory()

        # OIDC login
        session_token = self.openid_login(web_client, user)
        # Introspect AuthKey
        authkey_response = self.authkey_introspect(web_client, session_token)

        self.assertEqual(authkey_response.status_code, 200, "/authkey/introspect: response status code is not 200")
        self.assertIn('username', authkey_response.json(), "/authkey/introspect: username not in JSON response")
        self.assertIn('groups', authkey_response.json(), "/authkey/introspect: groups not in JSON response")
        self.assertEqual(authkey_response.json().get('username'), user.email, "/authkey/introspect: returned username is not equal user's email")
        self.assertEqual(['free'], authkey_response.json().get('groups'), "/authkey/introspect: 'free' not in user's groups")

    def test_validate_invalid_session_key(self):
        web_client = Client()

        # Introspect AuthKey
        authkey_response = self.authkey_introspect(web_client, 'some-random-auth-key')

        self.assertEqual(authkey_response.status_code, 404, "/authkey/introspect with invalid session_token: response status code is not 404")
        self.assertIn('username', authkey_response.json(), "/authkey/introspect with invalid session_token: username not in JSON response")
        self.assertIn('groups', authkey_response.json(), "/authkey/introspect with invalid session_token: groups not in JSON response")
        self.assertIsNone(authkey_response.json().get('username'), "/authkey/introspect with invalid session_token: username is not None")
        self.assertIsNone(authkey_response.json().get('groups'), "/authkey/introspect with invalid session_token: groups is not None")

    def test_validate_valid_session_key_user_with_multiple_groups(self):
        web_client = Client()
        user = UserFactory()

        # assign user to multiple groups
        Group.objects.get(name='pro').users.add(user)
        Group.objects.get(name='enterprise').users.add(user)

        # OIDC login
        session_token = self.openid_login(web_client, user)
        # Introspect AuthKey
        authkey_response = self.authkey_introspect(web_client, session_token)

        self.assertEqual(authkey_response.status_code, 200, "/authkey/introspect: response status code is not 200")
        self.assertIn('username', authkey_response.json(), "/authkey/introspect: username not in JSON response")
        self.assertIn('groups', authkey_response.json(), "/authkey/introspect: groups not in JSON response")
        self.assertEqual(authkey_response.json().get('username'), user.email, "/authkey/introspect: returned username is not equal user's email")
        # Watch out! Geoserver does not understand a list in classic approach, so it will be in ['free,pro,enterprise'] format!!
        self.assertIn('free', authkey_response.json().get('groups')[0], "/authkey/introspect: 'free' not in user's groups")
        self.assertIn('pro', authkey_response.json().get('groups')[0], "/authkey/introspect: 'pro' not in user's groups")
        self.assertIn('enterprise', authkey_response.json().get('groups')[0], "/authkey/introspect: 'enterprise' not in user's groups")

    def test_validate_valid_api_key(self):
        web_client = Client()
        user = UserFactory()
        api_key = ApiKeyFactory(user=user)

        # Introspect API key
        apikey_response = self.authkey_introspect(web_client, api_key.key)

        self.assertEqual(apikey_response.status_code, 200, "/authkey/introspect API key: response status code is not 200")
        self.assertIn('username', apikey_response.json(), "/authkey/introspect API key: username not in JSON response")
        self.assertIn('groups', apikey_response.json(), "/authkey/introspect API key: groups not in JSON response")
        self.assertEqual(apikey_response.json().get('username'), user.email, "/authkey/introspect API key: returned username is not equal user's email")
        self.assertIn('free', apikey_response.json().get('groups')[0], "/authkey/introspect API key: 'free' not in user's groups")

    def test_validate_revoked_api_key(self):
        web_client = Client()
        user = UserFactory()
        api_key = ApiKeyFactory(user=user, revoked=True)

        # Introspect API key
        apikey_response = self.authkey_introspect(web_client, api_key.key)

        self.assertEqual(apikey_response.status_code, 404, "/authkey/introspect revoked API key: response status code is not 200")
        self.assertIn('username', apikey_response.json(), "/authkey/introspect revoked API key: username not in JSON response")
        self.assertIn('groups', apikey_response.json(), "/authkey/introspect revoked API key: groups not in JSON response")
        self.assertIsNone(apikey_response.json().get('username'), "/authkey/introspect revoked API key: username in JSON response is not None")
        self.assertIsNone(apikey_response.json().get('groups'), "/authkey/introspect revoked API key: groups in JSON response is not None")

    def test_validate_valid_api_key_with_existing_session_key(self):
        web_client = Client()
        user = UserFactory()
        api_key = ApiKeyFactory(user=user)

        # OIDC login
        self.openid_login(web_client, user)
        # Introspect API key
        apikey_response = self.authkey_introspect(web_client, api_key.key)

        self.assertEqual(apikey_response.status_code, 200, "/authkey/introspect API key with existing SessionKey: response status code is not 200")
        self.assertIn('username', apikey_response.json(), "/authkey/introspect API key with existing SessionKey: username not in JSON response")
        self.assertIn('groups', apikey_response.json(), "/authkey/introspect API key with existing SessionKey: groups not in JSON response")
        self.assertEqual(apikey_response.json().get('username'), user.email, "/authkey/introspect API key with existing SessionKey: returned username is not equal user's email")
        self.assertIn('free', apikey_response.json().get('groups')[0], "/authkey/introspect API key with existing SessionKey: 'free' not in user's groups")

    def test_validate_valid_session_key_with_existing_api_key(self):
        web_client = Client()
        user = UserFactory()
        api_key = ApiKeyFactory(user=user)

        # OIDC login
        session_token = self.openid_login(web_client, user)
        # Introspect AuthKey
        authkey_response = self.authkey_introspect(web_client, session_token)

        self.assertEqual(authkey_response.status_code, 200, "/authkey/introspect Session key with existing API Key: response status code is not 200")
        self.assertIn('username', authkey_response.json(), "/authkey/introspect Session key with existing API Key: username not in JSON response")
        self.assertIn('groups', authkey_response.json(), "/authkey/introspect Session key with existing API Key: groups not in JSON response")
        self.assertEqual(authkey_response.json().get('username'), user.email, "/authkey/introspect Session key with existing API Key: returned username is not equal user's email")
        self.assertEqual(['free'], authkey_response.json().get('groups'), "/authkey/introspect Session key with existing API Key: 'free' not in user's groups")

    def test_validate_invalid_session_key_with_existing_api_key(self):
        web_client = Client()
        user = UserFactory()
        api_key = ApiKeyFactory(user=user)

        # Introspect AuthKey
        authkey_response = self.authkey_introspect(web_client, 'some-random-auth-key')

        self.assertEqual(authkey_response.status_code, 404, "/authkey/introspect revoked API key: response status code is not 200")
        self.assertIn('username', authkey_response.json(), "/authkey/introspect revoked API key: username not in JSON response")
        self.assertIn('groups', authkey_response.json(), "/authkey/introspect revoked API key: groups not in JSON response")
        self.assertIsNone(authkey_response.json().get('username'), "/authkey/introspect revoked API key: username in JSON response is not None")
        self.assertIsNone(authkey_response.json().get('groups'), "/authkey/introspect revoked API key: groups in JSON response is not None")

    # @skip("This test should be run only on server with unsecured HTTP")
    def test_require_https_for_geoserver_authkey_introspection(self):
        web_client = Client()
        user = UserFactory()

        # OIDC login
        session_token = self.openid_login(web_client, user)
        # Introspect AuthKey
        with self.settings(REQUIRE_SECURE_HTTP_FOR_GEOSERVER_INTROSPECTION=True):
            authkey_response = self.authkey_introspect(web_client, session_token)

        self.assertEqual(authkey_response.status_code, 400, "/authkey/introspect with HTTPS required: response status code is not 400")
        self.assertIn('username', authkey_response.json(), "/authkey/introspect: username not in JSON response")
        self.assertIn('groups', authkey_response.json(), "/authkey/introspect: groups not in JSON response")
        self.assertIsNone(authkey_response.json().get('username'), "/authkey/introspect: returned username is not None")
        self.assertIsNone(authkey_response.json().get('groups'), "/authkey/introspect: returned groups is not None")


class TestUserCredentialsValidation(TestCase):

    def validate_user_credentials(self, web_client, username, password):
        """
        Method validating user's credentials
        """
        return web_client.get(
            reverse('user_credentials_introspection'),
            {
                'u': username,
                'p': password,
            },
        )

    def test_user_credentials_validation_with_correct_credentials(self):
        web_client = Client()

        user_psw = 'some_password'
        user = UserFactory()
        user.set_password(user_psw)
        user.save()

        user_credentials_response = self.validate_user_credentials(web_client, user.username, user_psw)

        self.assertEqual(user_credentials_response.status_code, 200, "User credentials response: response status code is not 200")
        self.assertIn('username', user_credentials_response.json(), "User credentials response: username not in JSON response")
        self.assertEqual(user_credentials_response.json().get('username'), user.username, "User credentials response: username is wrong")
        self.assertIn('groups', user_credentials_response.json(), "User credentials response: groups not in JSON response")
        self.assertIsNotNone(user_credentials_response.json().get('username'), "User credentials response: returned username is None")
        self.assertIsNotNone(user_credentials_response.json().get('groups'), "User credentials response: returned groups is None")

    def test_user_credentials_validation_with_wrong_credentials(self):
        web_client = Client()

        user_psw = 'some_password'
        user = UserFactory()
        user.set_password(user_psw)
        user.save()

        user_credentials_response = self.validate_user_credentials(web_client, user.username, 'some-wrong-password')

        self.assertEqual(user_credentials_response.status_code, 200, "User credentials response: response status code is not 200")
        self.assertIn('username', user_credentials_response.json(), "User credentials response: username not in JSON response")
        self.assertIn('groups', user_credentials_response.json(), "User credentials response: groups not in JSON response")
        self.assertIsNone(user_credentials_response.json().get('username'), "User credentials response: returned username is not None")
        self.assertIsNone(user_credentials_response.json().get('groups'), "User credentials response: returned groups is not None")

    def test_require_https_for_user_credentials_validation(self):
        web_client = Client()

        user_psw = 'some_password'
        user = UserFactory()
        user.set_password(user_psw)
        user.save()

        with self.settings(REQUIRE_SECURE_HTTP_FOR_GEOSERVER_INTROSPECTION=True):
            user_credentials_response = self.validate_user_credentials(web_client, user.username, user_psw)

        self.assertEqual(user_credentials_response.status_code, 400, "User credentials response: response status code is not 400")
        self.assertIn('username', user_credentials_response.json(), "User credentials response: username not in JSON response")
        self.assertIn('groups', user_credentials_response.json(), "User credentials response: groups not in JSON response")
        self.assertIsNone(user_credentials_response.json().get('username'), "User credentials response: returned username is not None")
        self.assertIsNone(user_credentials_response.json().get('groups'), "User credentials response: returned groups is not None")
