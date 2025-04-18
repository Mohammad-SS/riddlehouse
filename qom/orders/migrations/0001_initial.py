# Generated by Django 4.1.1 on 2022-10-24 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_completed", models.BooleanField(default=False)),
                ("customer_name", models.CharField(max_length=255)),
                ("customer_mobile", models.CharField(max_length=15)),
                ("authority_key", models.CharField(max_length=255)),
                ("players_number", models.IntegerField()),
                ("amount", models.IntegerField()),
                ("used_coupon", models.CharField(blank=True, max_length=15, null=True)),
                ("reserved_time", models.DateTimeField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="payments",
                        to="game.room",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("customer_name", models.CharField(max_length=255)),
                ("customer_number", models.CharField(max_length=15)),
                ("transaction_number", models.CharField(max_length=255)),
                ("players_number", models.IntegerField()),
                ("paid", models.IntegerField()),
                ("key", models.CharField(max_length=4)),
                ("rest_payment", models.IntegerField()),
                ("used_coupon", models.CharField(blank=True, max_length=15, null=True)),
                (
                    "user_sms_bulk",
                    models.CharField(blank=True, max_length=31, null=True),
                ),
                (
                    "admin_sms_bulk",
                    models.CharField(blank=True, max_length=31, null=True),
                ),
                ("card_pan", models.CharField(blank=True, max_length=127, null=True)),
                ("reserved_time", models.DateTimeField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="orders",
                        to="game.room",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("P", "%"), ("C", "Const")], default="P", max_length=1
                    ),
                ),
                ("amount", models.IntegerField()),
                ("used", models.IntegerField(blank=True, null=True)),
                ("capacity", models.IntegerField()),
                (
                    "available_rooms",
                    models.ManyToManyField(related_name="coupons", to="game.room"),
                ),
            ],
        ),
    ]
