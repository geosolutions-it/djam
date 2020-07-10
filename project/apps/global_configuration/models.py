from django.db import models


class SingletonRawOperationError(Exception):
    pass


class SingletonQuerySet(models.query.QuerySet):

    def delete(self):
        raise SingletonRawOperationError('Deletion is not allowed')


class SingletonModelManager(models.Manager):

    def get_queryset(self):
        return SingletonQuerySet(self.model, using=self._db)

    def create(self, **obj_data):
        raise SingletonRawOperationError('Direct creation is not allowed in this kind of model')


class SingletonModel(models.Model):
    """
    Base, abstract class for django singleton models
    Note: when registering a Singleton model in admin panel, remember to restrict deletion permissions
    since deleting model will throw an exception
    """
    objects = SingletonModelManager()

    class Meta:
        abstract = True

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        kwargs.update({'force_insert': False})
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise SingletonRawOperationError('Method is not allowed in this kind of model')


class GlobalConfiguration(SingletonModel):
    navbar_redirect_url = models.URLField()
    map_redirect_url = models.URLField()

    class Meta:
        verbose_name_plural = 'Configuration'

    def __str__(self):
        return 'Configuration'
