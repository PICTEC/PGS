from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('parkings', '0012_parking_terminal'),
    ]

    operations = [
        migrations.AddField(
            model_name='parking',
            name='normalized_reg_num',
            field=models.CharField(
                blank=True, db_index=True, max_length=20,
                verbose_name='normalized registration number'),
        ),
    ]
