from django.test import TestCase

from apps.global_configuration.models import (
    GlobalConfiguration,
    SingletonRawOperationError,
)


class SingletonModelCRUDTest(TestCase):
    def test_create_configuration_with_load(self):
        expected_models_count = 1
        GlobalConfiguration.load()
        self.assertEquals(
            GlobalConfiguration.objects.all().count(), expected_models_count
        )
        GlobalConfiguration.load()
        self.assertEquals(
            GlobalConfiguration.objects.all().count(), expected_models_count
        )

    def test_create_configuration_with_create(self):
        self.assertRaises(
            SingletonRawOperationError,
            GlobalConfiguration.objects.create,
            navbar_redirect_url="https://google.com",
            map_redirect_url="https://google.com",
        )

    def test_delete_configuration(self):
        self.assertRaises(SingletonRawOperationError, GlobalConfiguration.load().delete)

    def test_query_set_delete_configuration(self):
        GlobalConfiguration.load()
        self.assertRaises(
            SingletonRawOperationError, GlobalConfiguration.objects.all().delete
        )
