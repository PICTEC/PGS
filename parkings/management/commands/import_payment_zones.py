from django.core.management.base import BaseCommand

from parkings.importers import PaymentZoneImporter


class Command(BaseCommand):
    help = 'Uses the PaymentZoneImporter to import payment zones.'

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

    def handle(self, *args, **options):
        PaymentZoneImporter(
            address=options['address'],
            type=options['type'],
            local=options['local'],
        ).import_payment_zones()
