from rest_framework import permissions
from rest_framework.routers import APIRootView, DefaultRouter

from .parking_area import PublicAPIParkingAreaViewSet
from .parking_area_statistics import PublicAPIParkingAreaStatisticsViewSet
from .payment_zone import PublicAPIPaymentZoneViewSet
from .region import PublicAPIRegionViewSet
from .terminal import PublicAPITerminalViewSet
from ..url_utils import versioned_url


class PublicApiRootView(APIRootView):
    permission_classes = [permissions.AllowAny]


class Router(DefaultRouter):
    APIRootView = PublicApiRootView


router = Router()
router.register(
    r'parking_area',
    PublicAPIParkingAreaViewSet, basename='parkingarea')
router.register(
    r'parking_area_statistics',
    PublicAPIParkingAreaStatisticsViewSet, basename='parkingareastatistics')
router.register(
    r'payment_zones',
    PublicAPIPaymentZoneViewSet, basename='paymentzone')
router.register(
    r'terminals',
    PublicAPITerminalViewSet, basename='terminal')
router.register(
    r'regions',
    PublicAPIRegionViewSet, basename='region'
)

app_name = 'public'
urlpatterns = [
    versioned_url('v1', router.urls),
]
