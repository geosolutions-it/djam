import os

# send an email to staff members when a new user register
IP_USER_REGISTRATION_NOTIFICATION = os.getenv('DJAM_IP_USER_REGISTRATION_NOTIFICATION', False)

# send an email to staff members when a new user confirms their email
IP_USER_EMAIL_CONFIRMATION_NOTIFICATION = os.getenv('DJAM_IP_USER_EMAIL_CONFIRMATION_NOTIFICATION', False)
