from django.core.management.base import BaseCommand

from parkings.importers import ParkingAreaImporter


class Command(BaseCommand):
    help = 'Uses the parking area importer to create and update parking areas'

    def add_arguments(self, parser):
        parser.add_argument(
            'address',
            type=str,
            help=('Addres from where get parking areas')
        )
        parser.add_argument(
            'type',
            type=str,
            default='GeoJSON',
            help=('Type of data, GeoJSON or WFS')
        )
        parser.add_argument(
            '--local',
            action='store_true',
            default=False,
            help=('If the address refer to file on local drive')
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            dest='overwrite',
            default=False,
            help=('Overwrite existing data. You may want to manually '
                  'inspect the data before doing this. Use with care!'),
        )

    def handle(self, *args, **options):
        ParkingAreaImporter(
            address=options['address'],
            type=options['type'],
            local=options['local'],
            overwrite=options['overwrite'],
        ).import_areas()
