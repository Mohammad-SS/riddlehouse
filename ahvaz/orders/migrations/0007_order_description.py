# Generated by Django 4.1.1 on 2022-11-29 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_coupon_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
