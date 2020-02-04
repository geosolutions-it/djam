import json
from argparse import FileType

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--data", type=FileType('r'), help="MapStand API JSON representation.")

    def handle(self, *args, **options):
        User = get_user_model()
        users = json.loads(options.get("data").read())
        for user in users:
            if User.objects.filter(email=user.get('email')).exists() or \
                    User.objects.filter(username=user.get('username')).exists():
                continue
            else:
                User.objects.create(email=user.get('email'), username=user.get('username'), is_active=True,
                                    email_confirmed=True)
