
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangorestangularjsboilerplate', '0006_uploadfileform'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvatarForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.FileField(upload_to=b'', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='uploadfileform',
            name='docfile',
            field=models.FileField(upload_to=b'documents/%Y/%m/%d', blank=True),
        ),
        migrations.AddField(
            model_name='userstatus',
            name='first_name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='userstatus',
            name='last_name',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
