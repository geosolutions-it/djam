from django.views import View
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from apps.identity_provider.forms import SignUpForm
from apps.identity_provider.tasks import email_user


class SignupView(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # send activation message
            subject = "Activate Your Account"
            message = render_to_string('account_activation_email.html', {
                'username': user.username,
                'domain': get_current_site(request).domain,
                'activation_code': user.useractivationcode.activation_code,
            })
            email_user.send(user.email, subject, message)

            return redirect('activation_msg_sent')
        else:
            return render(request, 'signup.html', {'form': SignUpForm(), 'errors': form.errors})
