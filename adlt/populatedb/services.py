from adlt.core import factories as core_factories


def populatedb():
    core_factories.AgentFactory.create_batch(10)
