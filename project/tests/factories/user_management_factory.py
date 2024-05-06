import factory

from django.contrib.auth import get_user_model

from apps.privilege_manager.models import Team


class AdminFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.LazyAttribute(lambda instance: instance.email)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("first_name")
    email = factory.Faker("email")
    email_confirmed = True
    is_active = True
    is_staff = True


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.LazyAttribute(lambda instance: instance.email)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("first_name")
    email = factory.Faker("email")
    email_confirmed = True
    is_active = True
    is_staff = False


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Faker("name")
