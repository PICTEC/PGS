import abc
import json
import requests

from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon

from ..models import EnforcementDomain


class GeoJsonImporter(metaclass=abc.ABCMeta):
    def __init__(self, srid=None, default_domain_code=None):
        self.srid = srid
        self.default_domain_code = default_domain_code

    def read_and_parse(self, geojson_file_path, geojson_file_url=None):
        if geojson_file_url is not None:
            r = requests.get(geojson_file_url, allow_redirects=True)
            open(geojson_file_path, 'wb+').write(r.content)
        with open(geojson_file_path, "rt") as file:
            root = json.load(file)
            for member in root['features']:
                yield self._parse_member(member)

    def _parse_member(self, member):
        props = member['properties']
        return dict(props, geom=self.get_polygons(member['geometry']))

    def get_polygons(self, geom):
        result = GEOSGeometry(json.dumps(geom))

        if isinstance(result, Polygon):
            result = MultiPolygon(result)

        if self.srid:
            result.srid = self.srid

        return result

    def get_default_domain(self):
        if self.default_domain_code:
            return EnforcementDomain.objects.get(code=self.default_domain_code)
        return EnforcementDomain.get_default_domain()
