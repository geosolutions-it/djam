from django.db import models

from apps.privilege_manager.models import Team

# Create your models here.

class Resource(models.Model):
    
    """
    A generic Resource model, that will be used by other components to implement rules-based access to their own resources and services
    A Resource will contain a generic "path" attribute, whose meaning is only known to the services (e.g. the Gateway app) that will use the rule.
    """
    
    name = models.CharField(verbose_name="Name")
    path = models.CharField(verbose_name="path")

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(verbose_name="Name")
    user = models.ManyToManyField("user_management.User", blank=True)
    team = models.ManyToManyField(Team, blank=True)


class AccessRule(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
