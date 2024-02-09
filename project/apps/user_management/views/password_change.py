from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect


class CustomPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "request": self.request,
        }
        form.save(**opts)
        return HttpResponseRedirect(self.get_success_url())
