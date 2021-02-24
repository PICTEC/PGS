from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    operations = [migrations.RunSQL('UPDATE parkings_parkingterminal SET location = ST_SetSRID(ST_MakePoint(ST_Y(location), ST_X(location)), ST_SRID(location)) where ST_X(location) > 50;')]