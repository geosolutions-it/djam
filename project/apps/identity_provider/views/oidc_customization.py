import re
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import ObjectDoesNotExist
from oidc_provider.views import AuthorizeView, TokenView

from apps.identity_provider.models import Session
from apps.privilege_manager.utils import has_login_permission


class AuthorizeViewWithSessionKey(AuthorizeView):
    """
    Authorize view storing OpenID code in session data
    """

    def get(self, request, *args, **kwargs):

        # in case user data are missing, stop the flow and force fix
        if request.user.is_authenticated and not self._user_claims_valid(request.user):
            return HttpResponseRedirect(
                request.user.get_absolute_url() + "?fix_error=1"
            )

        # limit login access to a Client application to only privileged users
        client_id = request.GET.get("client_id", None)

        if client_id is not None and not request.user.is_anonymous:

            has_permission, message = has_login_permission(request.user, client_id)

            if not has_permission:
                return render(
                    request,
                    "user_management/simple_message.html",
                    context={"error": message},
                )

        response = super().get(request, *args, **kwargs)
        self.update_session_with_code(response)

        return response

    def _user_claims_valid(self, user):
        return user.first_name and user.last_name and user.username

    def post(self, request, *args, **kwargs):

        # limit login access to a Client application to only privileged users
        client_id = request.POST.get("client_id", None)

        if client_id is not None and not request.user.is_anonymous:

            has_permission, message = has_login_permission(request.user, client_id)

            if not has_permission:
                return render(
                    request,
                    "user_management/simple_message.html",
                    context={"error": message},
                )

        response = super().post(request, *args, **kwargs)
        self.update_session_with_code(response)

        return response

    def update_session_with_code(self, response):
        """
        Function updating user djam session with Code value
        """
        if response.status_code == 302 and response.headers.get("Location", None):
            re_code = re.search(
                "code=(\w+)&*?", response.headers.get("Location", "")[1]
            )
            if re_code is None:
                re_code = re.search(
                    "code=(\w+)&*?", response.headers.get("Location", "")
                )

            if re_code is not None:
                code = re_code.groups()[0]
                session = Session.objects.get(
                    session_key=self.request.session.session_key
                )
                session.oidc_code = code
                session.save()


class StatelessAuthorizeView(AuthorizeViewWithSessionKey):
    """
    Authorize view which prevents sending empty state parameter.

    View prepared for integration with Geoserver, which does not send or check state, yet fails on response validation with empty state.
    """

    def get(self, *args, **kwargs):

        response = super().get(*args, **kwargs)

        if response.has_header("location"):
            # check if state param is empty
            location_header = response.headers["Location"]
            if re.search("&state=$", location_header) or re.search(
                "&state=&", response.location_header
            ):
                # remove empty state from redirect url
                response.headers["Location"] = (
                    "Location",
                    location_header.replace("&state=", ""),
                )

        return response


class TokenViewWithSessionKey(TokenView):
    """
    Token view with response extended with Session Token
    """

    def post(self, request, *args, **kwargs):
        code = request.POST.get("code", None)
        response = super().post(request, *args, **kwargs)

        # if response is correct, attach Session Token
        if response.status_code == 200 and code is not None:
            try:
                session = Session.objects.get(oidc_code=code)
            except ObjectDoesNotExist:
                return response

            data = json.loads(response.content)
            data["session_token"] = str(session.uuid)
            response.content = json.dumps(data)

        return response
