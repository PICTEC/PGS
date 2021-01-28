from django.core.management.base import BaseCommand

from parkings.importers import RegionImporter


class Command(BaseCommand):
    help = 'Uses the RegionImporter to import regions.'

    def add_arguments(self, parser):
        parser.add_argument('geojson_file_path')
        parser.add_argument('geojson_file_url', type=str, default=None)
        parser.add_argument('--srid', '-s', type=int, default=None)
        parser.add_argument('--domain', '-d', type=str, default=None)

    def handle(self, *, geojson_file_path, geojson_file_url=None,
               srid=None, domain=None, **kwargs):
        importer = RegionImporter(srid=srid, default_domain_code=domain)
        importer.import_regions(geojson_file_path, geojson_file_url)
