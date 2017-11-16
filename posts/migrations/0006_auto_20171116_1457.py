# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 14:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='publish_date',
            field=models.DateTimeField(default=datetime.date(2017, 11, 16)),
            preserve_default=False,
        ),
    ]
