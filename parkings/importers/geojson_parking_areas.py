import logging
import os

from django.db import transaction

from ..models import ParkingArea
from .geojson_importer import GeoJsonImporter

logger = logging.getLogger(__name__)

mydir = os.path.dirname(__file__)


class ParkingAreaImporter(GeoJsonImporter):
    """
    Imports parkingaraeas data
    """

    def import_parking_areas(self, geojson_file_path, geojson_file_url=None):
        parking_area_dicts = self.read_and_parse(geojson_file_path, geojson_file_url)
        count = self._save_parking_areas(parking_area_dicts)
        logger.info('Created or updated {} parking areas'.format(count))

    @transaction.atomic
    def _save_parking_areas(self, parking_area_dicts):
        logger.info('Saving parking areas.')
        default_domain = self.get_default_domain()
        count = 0
        parking_area_ids = []
        for area_dict in parking_area_dicts:
            domain = area_dict.pop('domain', default_domain)
            origin_id = area_dict.pop('origin_id', area_dict.get('origin_id'))
            capacity_estimate = area_dict.pop('capacity_estimate', area_dict.get('capacity_estimate'))
            parking_area, _ = ParkingArea.objects.update_or_create(
                origin_id=origin_id,
                capacity_estimate=capacity_estimate,
                domain=domain,
                defaults=area_dict)
            parking_area_ids.append(parking_area.pk)
            count += 1
        return count
