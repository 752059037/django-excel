# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2019-04-08 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0003_auto_20190408_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bx_everyday_contrast_data',
            name='include_num_contrast',
            field=models.FloatField(),
        ),
    ]
