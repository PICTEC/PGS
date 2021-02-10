from rest_framework import permissions, serializers, viewsets

from parkings.models import ParkingTerminal, EnforcementDomain
from parkings.pagination import Pagination


class TerminalSerializer(serializers.ModelSerializer):
    domain = serializers.SlugRelatedField(
        slug_field='code', queryset=EnforcementDomain.objects.all(),
        default=EnforcementDomain.get_default_domain)

    class Meta:
        model = ParkingTerminal
        fields = ['number', 'name', 'location', 'domain']


class PublicAPITerminalViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = ParkingTerminal.objects.order_by('number')
    serializer_class = TerminalSerializer
    pagination_class = Pagination
