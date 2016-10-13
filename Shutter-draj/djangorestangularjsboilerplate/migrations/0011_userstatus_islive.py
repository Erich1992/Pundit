# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangorestangularjsboilerplate', '0010_auto_20160523_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatus',
            name='isLive',
            field=models.BooleanField(default=False),
        ),
    ]
