# Generated by Django 4.0.1 on 2022-01-18 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_meter', '0002_rename_counter_meter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='meter',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_meter.unit'),
        ),
    ]
