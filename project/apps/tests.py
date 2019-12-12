"""
example client redirect URL:
http://localhost:8000/openid/authorize?response_type=code&client_id=641011&redirect_uri=http%3A%2F%2Flocalhost%3A8100%2Flogin_handler&scope=openid%20profile%20email&state=af0ifjsldkj
"""

import dramatiq

import requests


@dramatiq.actor(max_retries=3)
def count_words(url):
    response = requests.get(url)
    count = len(response.text.split(" "))
    print(f"There are {count} words at {url!r}.")

