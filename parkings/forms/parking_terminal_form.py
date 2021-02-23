import math
from typing import Optional

from django import forms

from parkings.models import ParkingTerminal
from django.contrib.gis.geos import Point


class ParkingTerminalForm(forms.ModelForm):
    latitude = forms.FloatField(
        min_value=-90,
        max_value=90,
        required=False,
    )
    longitude = forms.FloatField(
        min_value=-180,
        max_value=180,
        required=False,
    )

    class Meta:
        exclude = []
        model = ParkingTerminal

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coordinates = self.initial.get('location', None)
        if isinstance(coordinates, Point):
            self.initial['latitude'], self.initial['longitude'] = coordinates.tuple

    def clean(self):
        data = super().clean()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        point = data.get('location')
        if self._use_coordinates_instead_of_point(latitude, longitude, point):
            data['location'] = Point(x=latitude, y=longitude)
        return data

    def _use_coordinates_instead_of_point(self, latitude, longitude, point):
        coordinates_manually_set = latitude and longitude
        point_not_set = not point
        return coordinates_manually_set and (point_not_set or self._point_did_not_change(point))

    def _point_did_not_change(self, current_point: Point):
        initial_point: Optional[Point] = self.initial.get('location', None)
        if initial_point is None:
            return False
        current_coordinates = current_point.tuple
        initial_coordinates = initial_point.tuple
        longitude_not_changed = math.isclose(current_coordinates[0], initial_coordinates[0])
        latitude_not_changed = math.isclose(current_coordinates[1], initial_coordinates[1])
        return latitude_not_changed and longitude_not_changed
