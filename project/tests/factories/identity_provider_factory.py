import random
import factory
from oidc_provider import models as oidc_models

from tests.factories.user_management_factory import AdminFactory


class OIDCConfidentialClientFactory(factory.DjangoModelFactory):
    class Meta:
        model = oidc_models.Client

    name = factory.Faker('company')
    owner = factory.SubFactory(AdminFactory)
    client_id = str(random.randint(1, 999999)).zfill(6)
    client_secret = str(random.randint(1, 999999)).zfill(6)
    require_consent = False
    reuse_consent = True

    @factory.post_generation
    def _redirect_uris(self, create, extracted, **kwargs):
        self._redirect_uris = 'http://localhost:8100/login_handler'

    @factory.post_generation
    def _scope(self, create, extracted, **kwargs):
        _scope = 'openid profile user_id groups legacy_user_id'

    @factory.post_generation
    def response_types(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        # When creating an instance (saving to the DB), assign default 'code' value to available response_types
        self.response_types.add(oidc_models.ResponseType.objects.get(value='code'))
