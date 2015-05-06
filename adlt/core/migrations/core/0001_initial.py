# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json
import django.utils.timezone
import django_extensions.db.fields
from django.conf import settings
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('title', models.CharField(verbose_name='Pavadinimas/Vardas', max_length=255)),
                ('individual', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('title', models.CharField(verbose_name='Pavadinimas', max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='Aprašymas')),
                ('maturity_level', models.PositiveSmallIntegerField(choices=[(0, '0. Duomenys nėra pateikti'), (1, '1. Atvira licencija'), (2, '2. Struktūruoti duomenys'), (3, '3. Atviras formatas'), (4, '4. Adresuojami duomenys'), (5, '5. Susietieji duomenys')], verbose_name='Brandos lygis')),
                ('link', models.URLField(help_text='Nuoroda į vietą internete, kur pateikiami duomenys ar informacija apie duomenis.', verbose_name='Nuoroda', blank=True)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('agent', models.ForeignKey(to='core.Agent', verbose_name='Organizacija', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('object_type', models.CharField(choices=[('dataset', 'Dataset'), ('project', 'Project')], max_length=20)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('title', models.CharField(verbose_name='Pavadinimas', max_length=255)),
                ('description', models.TextField(verbose_name='Aprašymas')),
                ('datasets_links', models.TextField(verbose_name='Duomenų šaltiniai')),
                ('likes', models.PositiveIntegerField(default=0)),
                ('agent', models.ForeignKey(to='core.Agent', verbose_name='Organizacija/Asmnuo')),
                ('datasets', models.ManyToManyField(to='core.Dataset')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('url', django_extensions.db.fields.json.JSONField()),
                ('data', django_extensions.db.fields.json.JSONField()),
                ('context', django_extensions.db.fields.json.JSONField()),
                ('message', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
