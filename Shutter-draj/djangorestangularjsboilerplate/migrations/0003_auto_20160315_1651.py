# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangorestangularjsboilerplate', '0002_auto_20160315_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='like',
            name='liker',
        ),
        migrations.AddField(
            model_name='comment',
            name='like',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
