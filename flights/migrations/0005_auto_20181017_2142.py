# Generated by Django 2.1.2 on 2018-10-17 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0004_auto_20181017_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='flight_status',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='flights.FlightStatus'),
        ),
    ]