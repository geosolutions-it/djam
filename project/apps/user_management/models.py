from __future__ import unicode_literals

import uuid

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.user_management.model_managers import UserManager
from apps.user_management.utils import random_string


class CaseInsensitiveFieldMixin:
    """
    Field mixin that uses case-insensitive lookup alternatives if they exist.
    Note: Lookups that do not have case-insensitive versions (e.g. “in”) will not be case-insensitive.
    """
    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }

    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)


class CaseInsensitiveEmailField(CaseInsensitiveFieldMixin, models.EmailField):
    pass


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = CaseInsensitiveEmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    email_confirmed = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin sites.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    legacy_user_id = models.IntegerField(null=True, blank=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserActivationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_code = models.CharField(max_length=50, default=random_string)
    creation_date = models.DateTimeField(default=timezone.now)

    def regenerate_code(self):
        self.activation_code = random_string()
        self.creation_date = timezone.now()


@receiver(post_save, sender=User)
def create_activation_code(sender, instance, created, **kwargs):
    if created:
        UserActivationCode.objects.create(user=instance)
