# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangorestangularjsboilerplate', '0009_stream_watch_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatus',
            name='full_name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='userstatus',
            name='streams',
            field=models.IntegerField(default=0),
        ),
    ]
