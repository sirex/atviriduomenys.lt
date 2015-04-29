import mock
import unittest

from adlt.common.helpers.factories import fake


class FakerWrapperTests(unittest.TestCase):
    @mock.patch.object(fake.faker, 'company')
    def test_faker_wrapper(self, company):
        company.return_value = 'Durgan, Erdman and West'
        self.assertEqual(fake.company()(), 'Durgan, Erdman and West')
