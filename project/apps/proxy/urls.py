from django.urls import re_path
from apps.proxy.views import proxy_view


urlpatterns = [

# Main URL for the proxy app
re_path(r'service/(?P<request_path>.*)', proxy_view, name="proxy_view"),

]