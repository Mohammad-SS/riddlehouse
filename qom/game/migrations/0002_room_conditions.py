# Generated by Django 4.1.1 on 2022-10-24 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="conditions",
            field=models.TextField(blank=True, null=True),
        ),
    ]