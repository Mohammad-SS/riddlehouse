# Generated by Django 4.1.1 on 2023-10-28 12:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_remove_vipsans_dates_vipsans_from_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vipsans',
            name='hours',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=12), blank=True, null=True, size=None),
        ),
    ]
