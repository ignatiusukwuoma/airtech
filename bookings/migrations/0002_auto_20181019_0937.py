# Generated by Django 2.1.2 on 2018-10-19 08:37

import bookings.utils
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_booking', models.CharField(blank=True, default=bookings.utils.generate_uuid, max_length=32, unique=True)),
                ('contact_name', models.CharField(max_length=254)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Please enter a Nigerian mobile phone number', regex='^0\\d{10}$')])),
            ],
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_status',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='arrival_ticket_1',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='arrival_ticket_2',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='departure_ticket_1',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='departure_ticket_2',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='passenger_email',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='passenger_phone',
        ),
        migrations.AddField(
            model_name='ticket',
            name='trip',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookings.Trip'),
            preserve_default=False,
        ),
        migrations.RenameModel(
            old_name='TicketStatus',
            new_name='BookingStatus',
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.BookingStatus'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='booking',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookings.Booking'),
            preserve_default=False,
        ),
    ]