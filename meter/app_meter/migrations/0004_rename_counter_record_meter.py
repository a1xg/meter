# Generated by Django 4.0.1 on 2022-01-18 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_meter', '0003_unit_alter_meter_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='counter',
            new_name='meter',
        ),
    ]