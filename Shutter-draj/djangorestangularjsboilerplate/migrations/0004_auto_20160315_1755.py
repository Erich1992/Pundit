# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangorestangularjsboilerplate', '0003_auto_20160315_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatus',
            name='avatar',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='description',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='school',
            field=models.CharField(default=b'Unkonwn school', max_length=255),
        ),
    ]
