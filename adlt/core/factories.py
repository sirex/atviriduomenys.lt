import factory

from adlt.common.helpers.factories import fake

import adlt.core.models as core_models


class OrganizationFactory(factory.DjangoModelFactory):
    title = factory.LazyAttribute(fake.company())

    class Meta:
        model = core_models.Organization


class DatasetFactory(factory.DjangoModelFactory):
    title = factory.LazyAttribute(fake.company())

    class Meta:
        model = core_models.Dataset


class ProjectFactory(factory.DjangoModelFactory):
    title = factory.LazyAttribute(fake.company())

    class Meta:
        model = core_models.Project
