# Generated by Django 3.2 on 2021-05-11 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_utils', '0010_auto_20210510_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsonfeature',
            name='processed_time',
            field=models.DateTimeField(null=True),
        ),
    ]
