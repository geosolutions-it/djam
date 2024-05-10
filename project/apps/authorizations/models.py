from django.db import models

# Create your models here.


class Resource(models.Model):

    """
    A generic Resource model, that will be used by other components to implement rules-based access to their own resources and services
    A Resource will contain a generic "path" attribute, whose meaning is only known to the services (e.g. the Gateway app) that will use the rule.
    """
    class ResourceTypeEnum(models.TextChoices):
        UPSTREAM_SERVICE = "Upstream Service"

    URL_REQUIRED_SERVICE = [ResourceTypeEnum.UPSTREAM_SERVICE]

    name = models.CharField(verbose_name="Name")
    path = models.CharField(verbose_name="path")
    url = models.CharField(verbose_name="upstream url to be proxed to", null=True)
    type = models.CharField(
        max_length=100,
        choices=ResourceTypeEnum.choices,
        null=True,
        default=None
    )

    def __str__(self):
        return self.name

    def url_required(self):
        if self.type in self.URL_REQUIRED_SERVICE:
            return True
        return False

class Role(models.Model):
    name = models.CharField(verbose_name="Name", unique=True)

    def __str__(self):
        return self.name


class AccessRule(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.resource} | {self.role} | Active: {self.active}"
