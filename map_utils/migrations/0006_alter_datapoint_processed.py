# Generated by Django 3.2 on 2021-05-11 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_utils', '0005_datapoint_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapoint',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
