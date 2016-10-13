# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangorestangularjsboilerplate', '0005_auto_20160412_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFileForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
    ]
