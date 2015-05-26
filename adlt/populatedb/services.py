# pylint: disable=line-too-long

import django.contrib.auth.models as auth_models

from adlt.core import factories as core_factories


def populatedb():
    user = auth_models.User.objects.create_superuser(
        'superuser', 'superuser@example.com', 'secret', first_name='Super', last_name='User',
    )

    agent = core_factories.AgentFactory(title='Agent', user=user)

    seimas = core_factories.AgentFactory(title='Lietuvos Respublikos Seimas', user=user)
    ta = core_factories.DatasetFactory(title='Teisės aktų duomenys', maturity_level=1, agent=seimas, user=user)
    bd = core_factories.DatasetFactory(title='Balsavimų duomenys', maturity_level=1, agent=seimas, user=user)
    sn = core_factories.DatasetFactory(title='Seimo narių duomenys', maturity_level=1, agent=seimas, user=user)
    sd = core_factories.DatasetFactory(title='Seimo darbotvarkės duomenys', maturity_level=0, agent=seimas, user=user)

    rc = core_factories.AgentFactory(title='Registrų Centras', user=user)
    ad = core_factories.DatasetFactory(title='Adresų duomenys', maturity_level=0, agent=rc, user=user)

    archyvas = core_factories.AgentFactory(title='Lietuvos Istorijos Archyvas', user=user)
    md = core_factories.DatasetFactory(title='Gimimo, Mirties ir Santuokos metrikai', maturity_level=1, agent=archyvas, user=user)

    ms = core_factories.ProjectFactory(title='manoSeimas.lt', description='Aprašymas.', agent=agent, user=user)
    ms.datasets.add(ta)
    ms.datasets.add(bd)
    ms.datasets.add(sn)
    ms.datasets.add(sd)
    ms.datasets.add(ad)

    teisynas = core_factories.ProjectFactory(title='teisynas.lt', description='Aprašymas.', agent=agent, user=user)
    teisynas.datasets.add(ta)
    teisynas.datasets.add(sn)

    osm = core_factories.ProjectFactory(title='Open Street Map', description='Atviras žemėlapis', agent=agent, user=user)
    osm.datasets.add(ad)

    mskaitm = core_factories.ProjectFactory(title='Metrikų skaitmeninimas', description='Metrikų skaitmeninimas.', agent=agent, user=user)
    mskaitm.datasets.add(md)
    mskaitm.datasets.add(ad)
