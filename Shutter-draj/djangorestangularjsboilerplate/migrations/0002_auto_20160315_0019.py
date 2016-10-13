# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangorestangularjsboilerplate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='isLive',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='watch',
            field=models.IntegerField(default=0),
        ),
    ]
