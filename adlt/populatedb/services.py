from adlt.core.factories import OrganizationFactory


def populatedb():
    OrganizationFactory.create_batch(10)
