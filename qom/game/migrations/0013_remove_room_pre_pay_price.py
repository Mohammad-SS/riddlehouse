# Generated by Django 4.1.1 on 2022-12-10 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_room_admin_phones_room_pre_pay_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='pre_pay_price',
        ),
    ]