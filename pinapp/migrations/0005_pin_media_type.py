# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-11 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinapp', '0004_auto_20170811_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='media_type',
            field=models.CharField(default='image', help_text='The media type of the Pin (image or video).', max_length=5),
            preserve_default=False,
        ),
    ]
