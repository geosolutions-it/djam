import time
import logging
import requests

from django.conf import settings


logger = logging.getLogger(__name__)


def send_hubspot_notify(email, username, subscription, first_name, last_name):
    hubspot_url = settings.HUBSPOT_REGISTRATION_URL

    body = {
        "submittedAt": int(round(time.time() * 1000)),
        "fields": [
            {"name": "email", "value": email},
            {"name": "username", "value": username},
            {"name": "firstname", "value": first_name},
            {"name": "lastname", "value": last_name},
        ],
        "context": {
            "pageUri": "app.mapstand.com",
            "pageName": "MapStand Platform Application",
        },
        "legalConsentOptions": {
            "consent": {
                "consentToProcess": True,
                "text": "By clicking submit below, you consent to allow MapStand Limited to store and process the personal information submitted above to provide you the content requested.",
                "communications": [
                    {
                        "value": subscription,
                        "subscriptionTypeId": 5579305,
                        "text": "<p>By clicking 'Sign Up' below, you agree to the MapStand's <a href='   https://www.mapstand.com/terms/   ' rel='   noopener   '>Terms of Use</a>&nbsp; and <a href='   https://www.mapstand.com/privacy/   ' rel='   noopener   '>Privacy Policy</a></p>",
                    }
                ],
            }
        },
    }

    try:
        r = requests.post(url=hubspot_url, json=body)
        if r.status_code != 200:
            logger.error(
                f"Hubspot registration: Failed to send a post request to Hubspot url {hubspot_url}: status code: {r.status_code}: text: {r.text}"
            )
    except Exception as e:
        logger.error(
            f"Hubspot registration: Failed to send a post request to Hubspot url {hubspot_url}: Exception {e}"
        )


def register_login_in_hubspot(email):
    hubspot_url = f"https://track.hubspot.com/v1/event?_n={settings.HUBSPOT_LOGIN_EVENT_ID}&_a={settings.HUBSPOT_HUB_ID}&email={email}"
    try:
        r = requests.get(url=hubspot_url)
        if r.status_code != 200:
            logger.error(
                f"Hubspot registration: Failed to send a post request to Hubspot url {hubspot_url}: status code: {r.status_code}: text: {r.text}"
            )
    except Exception as e:
        logger.error(
            f"Hubspot registration: Failed to send a post request to Hubspot url {hubspot_url}: Exception {e}"
        )


def send_hubspot_update(instance):
    logging.debug(
        f'Hubspot updateing: Updating user information'
    )

