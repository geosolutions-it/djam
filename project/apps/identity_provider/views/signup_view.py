from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from apps.identity_provider.forms import SignUpForm
from apps.identity_provider.tasks import send_activation_email


class SignupView(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # compose activation link
            request_schema = 'https://' if request.is_secure() else 'http://'
            query_parameter = f'?activation_code={user.useractivationcode.activation_code}'
            activation_url = request_schema + get_current_site(request).domain + reverse('email_confirmation', kwargs={'user_uuid': user.uuid}) + query_parameter

            # send activation message
            send_activation_email.send(user.email, activation_url)

            return redirect('activation_msg_sent')
        else:
            return render(request, 'signup.html', {'form': SignUpForm(), 'errors': form.errors})
