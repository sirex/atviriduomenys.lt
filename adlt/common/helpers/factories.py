import faker


class FakerFactoryBoyWrapper(object):
    """Small wrapper around faker for factory boy.

    Usage:

        >>> from factory import LazyAttribute
        >>> from adlt.common.helpers.factories import fake
        >>> LazyAttribute(fake.company)  # doctest: +ELLIPSIS
        <factory.declarations.LazyAttribute object at 0x...>

    """

    def __init__(self):
        self.faker = faker.Factory.create()

    def __getattr__(self, name):
        faker = getattr(self.faker, name)

        def wrapper(*args, **kwargs):
            def func(obj=None):  # pylint: disable=unused-argument
                return faker(*args, **kwargs)
            return func

        return wrapper


fake = FakerFactoryBoyWrapper()  # pylint: disable=invalid-name
