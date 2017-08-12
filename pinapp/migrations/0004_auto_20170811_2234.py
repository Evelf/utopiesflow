# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-08-11 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinapp', '0003_auto_20160521_0139'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='boardtranslation',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='boardtranslation',
            name='master',
        ),
        migrations.AddField(
            model_name='board',
            name='name',
            field=models.CharField(default='default', help_text='The name of the board.', max_length=50),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='BoardTranslation',
        ),
    ]
