# Generated by Django 4.1.1 on 2022-11-09 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_order_package_payment_package_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="players_number",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
