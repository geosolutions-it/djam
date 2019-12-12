from datetime import timedelta
from django.views import View
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import get_user_model
from apps.identity_provider.models import UserActivationCode


class EmailConfirmationView(View):

    def get(self, request, user_uuid, *args, **kwargs):
        activation_code = request.GET.get('activation_code')

        user = get_user_model().objects.filter(uuid=user_uuid).first()

        if user is None:
            return self.render_error(request, 'Resource not found.')

        if user.email_confirmed:
            return self.render_error(request, 'Email already confirmed')

        user_activation_code = UserActivationCode.objects.filter(activation_code=activation_code).first()
        if user_activation_code is None:
            return self.render_error(request, 'Resource not found: most likely activation code already used.')

        if user_activation_code.user.id != user.id:
            return self.render_error(request, 'User activation code mismatch')

        code_expired = timedelta(hours=settings.IP_ACTIVATION_CODE_EXPIRATION_HOURS) < (timezone.now() - user_activation_code.creation_date)

        if code_expired:
            return self.render_error(request, 'Activation code expired.')

        user_activation_code.user.email_confirmed = True
        user_activation_code.user.save()

        user_activation_code.delete()

        return render(
            request,
            'email_confirmed.html'
        )

    def render_error(self, request, error):
        return render(
            request,
            'email_confirmation_error.html',
            context={'error': error}
        )
