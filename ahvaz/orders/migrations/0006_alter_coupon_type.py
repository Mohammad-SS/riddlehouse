# Generated by Django 4.1.1 on 2022-11-14 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_players_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='type',
            field=models.CharField(choices=[('P', 'percent'), ('C', 'const')], default='P', max_length=1),
        ),
    ]
