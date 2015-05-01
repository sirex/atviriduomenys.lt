import factory

from adlt.common.helpers.factories import fake

import adlt.core.models as core_models


class AgentFactory(factory.DjangoModelFactory):
    title = factory.LazyAttribute(fake.company())
    active = True

    class Meta:
        model = core_models.Agent


class DatasetFactory(factory.DjangoModelFactory):
    title = factory.LazyAttribute(fake.company())
    maturity_level = core_models.Dataset.OPEN_FORMAT

    class Meta:
        model = core_models.Dataset


class ProjectFactory(factory.DjangoModelFactory):
    title = factory.LazyAttribute(fake.company())

    class Meta:
        model = core_models.Project
