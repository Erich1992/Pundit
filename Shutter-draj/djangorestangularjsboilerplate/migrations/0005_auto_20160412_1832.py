# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangorestangularjsboilerplate', '0004_auto_20160315_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='enable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(related_name='follower', to='djangorestangularjsboilerplate.UserStatus'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='leader',
            field=models.ForeignKey(related_name='leader', to='djangorestangularjsboilerplate.UserStatus'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='streamer',
            field=models.OneToOneField(related_name='streamer1', to='djangorestangularjsboilerplate.UserStatus'),
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='avatar',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='school',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
