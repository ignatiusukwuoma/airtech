# Generated by Django 2.1.2 on 2018-12-04 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0009_auto_20181028_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='reminder_sent',
            field=models.BooleanField(default=False),
        ),
    ]