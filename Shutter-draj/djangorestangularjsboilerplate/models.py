import hashlib

from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from djangorestangularjsboilerplate.utils.token import generate
from djangorestangularjsboilerplate.utils.email import send_activation_email
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.contrib.auth.models import User

class UserStatus(models.Model):
	user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	activation_token = models.CharField(max_length=255)
	school = models.CharField(max_length=255, blank=True)
	description = models.TextField(blank=True)
	avatar = models.CharField(max_length=255, blank=True)
	watch = models.IntegerField(default=0)
	first_name = models.CharField(max_length=255, blank=True)
	last_name = models.CharField(max_length=255, blank=True)
	full_name = models.CharField(max_length=255, blank=True)
	streams = models.IntegerField(default=0)
	isLive = models.BooleanField(default=False)
	class Meta:
		verbose_name_plural = "User Status"
	def __unicode__(self):
		return self.user.email
	def __str__(self):
		return self.user.email
	@receiver(post_save, sender = User)
	def create_user_instance(sender, instance, created = False, **kwargs):
		if not instance:
			return
		if hasattr(instance, '_dirty'):
			return
		try:
			status = UserStatus.objects.get(pk=instance.id)
		except ObjectDoesNotExist:
			token = generate(instance.email)
			userStatus = UserStatus(user = instance, id = instance.id, is_active=False, activation_token=token)
			userStatus.save()
			email_status = send_activation_email(userStatus)
			instance.is_active = True
			instance._dirty = True
			instance.save()
			stream = Stream(streamer = userStatus, id = instance.id, isLive = 0, watch_count = 0)
			stream.save()
			del instance._dirty

class Follow(models.Model):
	follower = models.ForeignKey(UserStatus, related_name='follower', on_delete=models.CASCADE)
	leader = models.ForeignKey(UserStatus, related_name='leader', on_delete=models.CASCADE)
	enable = models.BooleanField(default=True)

class Stream(models.Model):
	streamer = models.OneToOneField(UserStatus, related_name='streamer1')
	streamUrl = models.CharField(max_length =255)
	isLive = models.IntegerField(default = 0)
	watch_count = models.IntegerField(default = 0)

class Comment(models.Model):
	stream = models.ForeignKey(Stream, related_name='comments', on_delete=models.CASCADE)
	commenter = models.ForeignKey(UserStatus, related_name='commenter1')
	content = models.TextField(blank=True)
	like = models.BooleanField(default = False)

class AvatarForm(models.Model):
    image = models.FileField(blank=True)

# class UploadFileForm(models.Model):
#     docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank=True)

# class Like(models.Model):
# 	comment = models.ForeignKey('Comment', related_name='comment1')
# 	liker = models.ForeignKey('UserStatus', related_name='liker1')
# datetime = models.DateTimeField()
