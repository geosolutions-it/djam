from django.views import View
from django.shortcuts import render


class ActivationMsgSentView(View):

    def get(self, request):
        return render(request, 'activation_msg_sent.html')
