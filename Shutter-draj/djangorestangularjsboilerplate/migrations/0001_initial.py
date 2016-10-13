# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.ForeignKey(related_name='comment1', to='djangorestangularjsboilerplate.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('streamUrl', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('activation_token', models.CharField(max_length=255)),
                ('school', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('avatar', models.CharField(max_length=255)),
                ('watch', models.IntegerField()),
                ('user', models.OneToOneField(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Status',
            },
        ),
        migrations.AddField(
            model_name='stream',
            name='streamer',
            field=models.ForeignKey(related_name='streamer1', to='djangorestangularjsboilerplate.UserStatus'),
        ),
        migrations.AddField(
            model_name='like',
            name='liker',
            field=models.ForeignKey(related_name='liker1', to='djangorestangularjsboilerplate.UserStatus'),
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(related_name='follower1', to='djangorestangularjsboilerplate.UserStatus'),
        ),
        migrations.AddField(
            model_name='follow',
            name='leader',
            field=models.ForeignKey(related_name='leader1', to='djangorestangularjsboilerplate.UserStatus'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(related_name='commenter1', to='djangorestangularjsboilerplate.UserStatus'),
        ),
        migrations.AddField(
            model_name='comment',
            name='stream',
            field=models.ForeignKey(related_name='comments', to='djangorestangularjsboilerplate.Stream'),
        ),
    ]
