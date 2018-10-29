# Generated by Django 2.1.2 on 2018-10-27 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_auto_20181027_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='booking',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookings.Booking'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.TicketClass'),
        ),
    ]