import django.test

import adlt.core.factories as core_factories
import adlt.frontpage.services as frontpage_services


class ServiceTests(django.test.TestCase):
    # pylint: disable=invalid-name
    def test_orgstats(self):
        org1 = core_factories.OrganizationFactory(title='Org 1')
        o1ds1 = core_factories.DatasetFactory(organization=org1, maturity_level=1)
        o1ds2 = core_factories.DatasetFactory(organization=org1, maturity_level=2)
        o1ds3 = core_factories.DatasetFactory(organization=org1, maturity_level=3)

        org2 = core_factories.OrganizationFactory(title='Org 2')
        o2ds1 = core_factories.DatasetFactory(organization=org2, maturity_level=3)
        core_factories.DatasetFactory(organization=org2, maturity_level=4)

        p1, p2, p3 = core_factories.ProjectFactory.create_batch(3)

        p1.datasets.add(o1ds1)
        p1.datasets.add(o2ds1)
        p2.datasets.add(o1ds1)
        p2.datasets.add(o1ds2)
        p3.datasets.add(o1ds3)

        self.assertEqual(list(frontpage_services.orgrating().values_list('usage', 'projects', 'stars', 'title')), [
            (4, 3, 1.75, 'Org 1'),
            (1, 1, 3.5, 'Org 2'),
        ])
