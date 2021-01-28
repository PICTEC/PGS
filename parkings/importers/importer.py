import abc
import logging

from django.contrib.gis.geos import MultiPolygon, Point, Polygon
from lxml import etree
from owslib.wfs import WebFeatureService

import requests

logger = logging.getLogger(__name__)


class Importer(metaclass=abc.ABCMeta):
    wfs_url = 'https://kartta.hel.fi/ws/geoserver/avoindata/wfs'
    ns = {
        'wfs': 'http://www.opengis.net/wfs/2.0',
        'avoindata': 'https://www.hel.fi/avoindata',
        'gml': 'http://www.opengis.net/gml/3.2',
    }

    @property
    @abc.abstractmethod
    def wfs_typename(self):
        pass

    def download_and_parse(self):
        response = self._download()
        return self._parse_response(response)

    def download_geojson(self, url, path):
        r = requests.get(url, allow_redirects=True)
        open(path, 'wb').write(r.content)

    def _download(self):
        logger.info('Getting data from the server.')

        wfs = WebFeatureService(url=self.wfs_url, version='2.0.0')
        response = wfs.getfeature(typename=self.wfs_typename)
        return bytes(response.getvalue(), 'UTF-8')

    def _parse_response(self, content):
        logger.info('Parsing Data.')
        root = etree.fromstring(content)
        for member in root.findall('wfs:member', self.ns):
            yield self._parse_wfs_member(member)

    @abc.abstractmethod
    def _parse_wfs_member(self, member):
        pass

    def get_polygons(self, geom):
        """
        Turns the XML containing coordinates into a multipolygon
        """
        polygons = []

        for pos in geom.iter('*'):
            # get leaf nodes. Treat LinearRing and MultiSurface the same way
            if len(pos) == 0:
                positions = list(filter(None, pos.text.split(' ')))
                points = []
                points_as_pairs = zip(positions[1::2], positions[::2])
                for latitude, longitude in points_as_pairs:
                    points.append(Point(float(latitude), float(longitude)))
                polygons.append(Polygon(points))

        return MultiPolygon(polygons)
