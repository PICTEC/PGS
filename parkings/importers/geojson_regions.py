import logging
import os

from django.db import transaction

from ..models import Region
from .geojson_importer import GeoJsonImporter

logger = logging.getLogger(__name__)

mydir = os.path.dirname(__file__)


class RegionImporter(GeoJsonImporter):
    """
    Imports regions data
    """

    def import_regions(self, geojson_file_path, geojson_file_url=None):
        region_dicts = self.read_and_parse(geojson_file_path, geojson_file_url)
        count = self._save_regions(region_dicts)
        logger.info('Created or updated {} regions'.format(count))

    @transaction.atomic
    def _save_regions(self, region_dicts):
        logger.info('Saving regions.')
        default_domain = self.get_default_domain()
        count = 0
        region_ids = []
        for region_dict in region_dicts:
            domain = region_dict.pop('domain', default_domain)
            name = region_dict.pop('name', region_dict.get('name'))
            capacity_estimate = region_dict.pop('capacity_estimate', region_dict.get('capacity_estimate'))
            region, _ = Region.objects.update_or_create(
                name=name,
                capacity_estimate=capacity_estimate,
                domain=domain,
                defaults=region_dict)
            region_ids.append(region.pk)
            count += 1
        return count
