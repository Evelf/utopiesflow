# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinapp', '0006_auto_20170812_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='imported_at',
            field=models.DateTimeField(default='2017-08-12 00:00:00', help_text='The date the Pin was imported.', verbose_name='imported at'),
            preserve_default=False,
        ),
    ]
