# Generated by Django 3.2 on 2021-05-11 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_utils', '0004_jsonfeature'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='processed',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
