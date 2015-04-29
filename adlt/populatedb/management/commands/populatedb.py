from django.core.management.base import BaseCommand

from adlt.populatedb import services


class Command(BaseCommand):
    help = 'Populate database with sample data.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        services.populatedb()
