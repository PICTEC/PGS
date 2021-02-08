from rest_framework.routers import DefaultRouter

from .statistics import StatisticsExportView
from ..url_utils import versioned_url
from .region import RegionViewSet
from .region_statistics import RegionStatisticsViewSet
from .valid_parking import ValidParkingViewSet

router = DefaultRouter()
router.register(r'region', RegionViewSet, basename='region')
router.register(r'region_statistics', RegionStatisticsViewSet,
                basename='regionstatistics')
router.register(r'valid_parking', ValidParkingViewSet,
                basename='valid_parking')
router.register(r'statistics', StatisticsExportView, basename='statistics')

app_name = 'monitoring'
urlpatterns = [
    versioned_url('v1', router.urls),
]
