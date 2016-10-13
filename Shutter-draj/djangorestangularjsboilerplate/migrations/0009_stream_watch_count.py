# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangorestangularjsboilerplate', '0008_delete_uploadfileform'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='watch_count',
            field=models.IntegerField(default=0),
        ),
    ]
