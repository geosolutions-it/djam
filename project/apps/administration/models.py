from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class AbstractBaseModel(models.Model):
    class Meta:
        abstract = True


class ClientManagementModel(AbstractBaseModel):
    email = models.EmailField(_('email address'), blank=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    class Meta:
        verbose_name = _("Client Management")
        verbose_name_plural = _("Client Management")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        # Assign unique user email to username field - for django integrity, since Djam is not to use usernames
        self.username = self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
