from rest_framework import permissions, viewsets, serializers
from rest_framework_gis.fields import GeometrySerializerMethodField
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from parkings.api.common import WGS84InBBoxFilter
from parkings.api.monitoring.region import M2_PER_KM2
from parkings.models import PaymentZone, EnforcementDomain


class PaymentZoneSerializer(GeoFeatureModelSerializer):
    domain = serializers.SlugRelatedField(
        slug_field='code', queryset=EnforcementDomain.objects.all(),
        default=EnforcementDomain.get_default_domain)

    wgs84_geometry = GeometrySerializerMethodField()
    area_km2 = serializers.SerializerMethodField()

    def get_wgs84_geometry(self, instance):
        return instance.geom.transform(4326, clone=True)

    def get_area_km2(self, instance):
        return instance.geom.area / M2_PER_KM2

    class Meta:
        model = PaymentZone
        geo_field = 'wgs84_geometry'
        fields = ['number', 'name', 'domain', 'area_km2']


class PublicAPIPaymentZoneViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = PaymentZone.objects.order_by('code')
    serializer_class = PaymentZoneSerializer
    pagination_class = GeoJsonPagination
    bbox_filter_field = 'geom'
    filter_backends = [WGS84InBBoxFilter]
    bbox_filter_include_overlapping = True
