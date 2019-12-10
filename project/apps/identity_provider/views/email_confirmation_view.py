from datetime import timedelta
from django.views import View
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from apps.identity_provider.models import UserActivationCode


class EmailConfirmationView(View):

    def get(self, request, *args, **kwargs):
        activation_code = request.GET.get('activation_code')

        try:
            user_activation_code = UserActivationCode.objects.get(activation_code=activation_code)
        except Exception:
            # TODO: replace with HTMP error page
            return HttpResponse('Resource not found: most likely activation code already used.', status=404)

        code_expired = timedelta(hours=settings.ACTIVATION_CODE_EXPIRATION_HOURS) < (timezone.now() - user_activation_code.creation_date)

        if user_activation_code.deactivated or code_expired:
            # TODO: replace with HTMP error page
            return HttpResponse('Wrong resource state: activation code already used.', status=406)

        user_activation_code.user.email_confirmed = True
        user_activation_code.user.save()

        user_activation_code.delete()

        # TODO: replace with welcome page
        # return render(request, 'account_activation_success.html')
        return HttpResponse('Email confirmed', status=200)
