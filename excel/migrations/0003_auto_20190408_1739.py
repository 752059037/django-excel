# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2019-04-08 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0002_auto_20190408_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bx_everyday_contrast_data',
            name='brand_id',
            field=models.IntegerField(max_length=20),
        ),
    ]
