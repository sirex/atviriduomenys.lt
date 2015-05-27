# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150526_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='sources',
            field=models.ManyToManyField(to='core.Dataset', verbose_name='Pirminiai duomenų šaltiniai', related_name='datasets'),
        ),
    ]
