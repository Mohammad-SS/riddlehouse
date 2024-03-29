# Generated by Django 4.1.1 on 2022-12-14 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_alter_room_admin_phones'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimeExclusion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(blank=True, null=True)),
                ('closed', models.BooleanField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otes', to='game.room')),
            ],
        ),
    ]
