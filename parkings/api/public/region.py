import rest_framework_gis.pagination as gis_pagination
from rest_framework import viewsets, permissions

from ..common import WGS84InBBoxFilter
from ..monitoring.region import RegionSerializer
from ...models import Region


class PublicAPIRegionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Region.objects.all().order_by('id')
    serializer_class = RegionSerializer
    pagination_class = gis_pagination.GeoJsonPagination
    bbox_filter_field = 'geom'
    filter_backends = [WGS84InBBoxFilter]
    bbox_filter_include_overlapping = True
