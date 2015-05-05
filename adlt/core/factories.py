import factory

import django.contrib.auth.models as auth_models

import adlt.core.models as core_models
from adlt.common.helpers.factories import fake


class UserFactory(factory.DjangoModelFactory):
    username = 'u1'
    first_name = 'U1'
    last_name = 'User'
    is_superuser = False

    class Meta:
        model = auth_models.User
        django_get_or_create = ('username',)


class AgentFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(fake.company())
    active = True

    class Meta:
        model = core_models.Agent


class DatasetFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(fake.company())
    maturity_level = core_models.Dataset.OPEN_FORMAT

    class Meta:
        model = core_models.Dataset


class ProjectFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(fake.company())

    class Meta:
        model = core_models.Project
