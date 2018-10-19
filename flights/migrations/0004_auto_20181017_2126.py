# Generated by Django 2.1.2 on 2018-10-17 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0003_aircraft_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='flight_duration',
            field=models.DurationField(blank=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='last_update',
            field=models.DateTimeField(blank=True),
        ),
    ]
