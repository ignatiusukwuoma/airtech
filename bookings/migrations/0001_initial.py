# Generated by Django 2.1.2 on 2018-10-12 07:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_class', models.CharField(choices=[('E', 'Economy'), ('B', 'Business')], default='E', max_length=1)),
                ('e_ticket', models.CharField(blank=True, max_length=10, unique=True)),
                ('issue_date', models.DateField(auto_now_add=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.Flight')),
            ],
        ),
        migrations.CreateModel(
            name='TicketStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_name', models.CharField(max_length=254)),
                ('passenger_dob', models.DateField()),
                ('passenger_email', models.EmailField(max_length=254)),
                ('passenger_phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Enter a Nigerian mobile phone number', regex='^0\\d{10}$')])),
                ('arrival_ticket_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='d_ticket_1', to='bookings.Ticket')),
                ('arrival_ticket_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='d_ticket_2', to='bookings.Ticket')),
                ('departure_ticket_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='a_ticket_1', to='bookings.Ticket')),
                ('departure_ticket_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='a_ticket_2', to='bookings.Ticket')),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.TicketStatus'),
        ),
    ]
