# Generated by Django 4.1.1 on 2022-11-09 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_alter_coupon_used_alter_order_rest_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="package",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="package",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="payment",
            name="players_number",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]