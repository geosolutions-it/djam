import time
import jwt
import uuid

from django.http import HttpResponseRedirect
from django.views.generic import View
from django.conf import settings


class ZendeskSigninRedirect(View):
    def get(self, request, *args, **kwargs):
        redirect_location = self._zendesk_redirect(request)
        return HttpResponseRedirect(redirect_location)

    def _zendesk_redirect(self, request):
        payload = {
            "iat": int(time.time()),
            "jti": str(uuid.uuid1()),
            "name": request.user.get_full_name(),
            "email": request.user.email,
        }

        subdomain = settings.ZENDESK_SUBDOMAIN
        shared_key = settings.ZENDESK_SECRET

        jwt_value = jwt.encode(payload, shared_key)
        location = f"https://{subdomain}.zendesk.com/access/jwt?jwt={jwt_value}"
        return location
