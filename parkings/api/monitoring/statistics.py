import csv
from typing import List

from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets

from parkings.api.utils import parse_timestamp_or_now
from parkings.models import Parking
from .permissions import IsMonitor

class StatisticsExportView(viewsets.ViewSet):
    permission_classes = [IsMonitor]
    csv_headers = ["Operator name", "Payment zone", "Region name", "Parking area", "Terminal name", "Terminal number",
                   "Parking registration number"]

    def list(self, response):
        time_param = parse_timestamp_or_now(self.request.query_params.get('time'))
        time = time_param if time_param else timezone.now()

        http_response = HttpResponse(content_type='application/octet-stream')
        http_response['Content-Disposition'] = 'attachment; filename="statistics.csv"'

        writer = csv.writer(http_response, delimiter=";")
        parking_list = Parking.objects.filter(time_start__lt=time,
                                               time_end__gt=time)

        writer.writerow(self.csv_headers)
        for parking in parking_list:
            writer.writerow(self.map_parking_to_csv_row(parking))

        return http_response

    def map_parking_to_csv_row(self, parking) -> List[str]:
        return [
            parking.operator.name if parking.operator else "",
            parking.zone.name if parking.zone else "",
            parking.region.name if parking.region else "",
            parking.parking_area,
            parking.terminal.name if parking.terminal else "",
            parking.terminal_number,
            parking.registration_number
        ]