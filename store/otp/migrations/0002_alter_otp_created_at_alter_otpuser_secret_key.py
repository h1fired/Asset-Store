# Generated by Django 4.2.1 on 2023-05-19 19:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 19, 5, 58, 365931, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='otpuser',
            name='secret_key',
            field=models.CharField(default='GBIDOGIW7ZD7WQTUNU3BXDSRVB354XTG', max_length=32),
        ),
    ]