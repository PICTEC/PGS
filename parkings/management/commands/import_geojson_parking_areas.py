from django.core.management.base import BaseCommand

from parkings.importers import ParkingAreaImporter


class Command(BaseCommand):
    help = 'Uses the ParkingAreaImporter to import parking areas.'

    def add_arguments(self, parser):
        parser.add_argument('geojson_file_path')
        parser.add_argument('geojson_file_url', type=str, default=None)
        parser.add_argument('--srid', '-s', type=int, default=None)
        parser.add_argument('--domain', '-d', type=str, default=None)

    def handle(self, *, geojson_file_path, geojson_file_url=None,
               srid=None, domain=None, **kwargs):
        importer = ParkingAreaImporter(srid=srid, default_domain_code=domain)
        importer.import_parking_areas(geojson_file_path, geojson_file_url)
