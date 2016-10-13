import json

from braces.views import CsrfExemptMixin
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, list_route, detail_route
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from djangorestangularjsboilerplate.permissions import IsUserOrReadOnly
from djangorestangularjsboilerplate.utils.email import send_activation_email

from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from djoser.utils import decode_uid
from djoser.views import PasswordResetView as DjoserPasswordResetView
from social.actions import do_complete

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from oauth2_provider.views import TokenView

from django.views.decorators.csrf import csrf_exempt

from push_notifications.models import APNSDevice

from djangorestangularjsboilerplate.serializers import UserSerializer
from djangorestangularjsboilerplate.serializers import UserStatusSerializer
from djangorestangularjsboilerplate.serializers import ProfileSerializer
from djangorestangularjsboilerplate.serializers import FollowSerializer
from djangorestangularjsboilerplate.serializers import CommentSerializer
from djangorestangularjsboilerplate.serializers import StreamSerializer
from djangorestangularjsboilerplate.serializers import APNSDeviceSerializer
from djangorestangularjsboilerplate.serializers import AvatarSerializer

from rest_framework import filters
from rest_framework import generics

from djangorestangularjsboilerplate.models import UserStatus
from djangorestangularjsboilerplate.models import Follow
from djangorestangularjsboilerplate.models import Comment
from djangorestangularjsboilerplate.models import Stream
from djangorestangularjsboilerplate.models import AvatarForm

from push_notifications.models import APNSDevice

class APNS_StopView(View):
	def get(self, request, user_id):
		stream_id = request.GET.get('stream_id')
		stream = Stream.objects.get(pk = stream_id)
		if not stream_id:
			message = 'stream_id field is required'
			response = HttpResponse(
						json.dumps({'message': message}),
						content_type='application/json',
						)
			response.status_code = status.HTTP_200_OK
			return response
		devices = APNSDevice.objects.all()
		# for device in devices:
		# 	# device.send_message(name + " has stopped recording.")
		# 	device.send_message(" has stopped recording.")
		# return HttpResponse("")
		broadcaster = UserStatus.objects.get(id = user_id)
		follows = Follow.objects.filter(leader = user_id)
		for follow in follows:
			user = follow.follower
			try:
				devices = APNSDevice.objects.filter(user__id = user.id)
				for device in devices:
					device.send_message(broadcaster.full_name + " is live tune in!", extra={"stream": StreamSerializer(stream).data})
			except APNSDevice.DoesNotExist:
				continue
		print(follows.count())
		return HttpResponse(follows.count())

class IndexView(TemplateView):
	template_name = 'djangorestangularjsboilerplate/index.html'
	@method_decorator(ensure_csrf_cookie)
	def dispatch(self, *args, **kwargs):
		return super(IndexView, self).dispatch(*args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(IndexView, self).get_context_data(*args, **kwargs)
		context['FB_APP_ID'] = settings.SOCIAL_AUTH_FACEBOOK_KEY
		return context

class UserViewSet(viewsets.ModelViewSet):
	# permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly)
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

class UserStatusViewSet(viewsets.ModelViewSet):
	# permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly)
	queryset = UserStatus.objects.all()
	serializer_class = UserStatusSerializer
	renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('watch',)

	@detail_route(methods=['get'])
	def activate(self, request, pk=None):
		message = ''
		if 'token' not in request.query_params:
			message = 'token field is required'
		else:
			token = request.query_params.get('token')
			try:
				userStatus = self.get_object()
				if token != userStatus.activation_token:
					message = 'Invalid Token'
				elif userStatus.is_active:
					message = 'User already active'
				else:
					userStatus.is_active= True
					userStatus.save()
					userStatus.user.is_active=True
					userStatus.user.save()
					message = 'Account activated successfully'
			except ObjectDoesNotExist:
				message = 'User does not exist'
		return Response(
			{'message': message},
			template_name='djangorestangularjsboilerplate/account-activate/base.html'
			)
	@detail_route(methods=['get'])
	def send_activation_link(self, request, pk=None):
		if pk is None:
			Response({"pk": "this attribute is required"}, status=status.HTTP_400_BAD_REQUEST)
		user_status = self.get_object()
		email_status = send_activation_email(user_status)
		print 'sending activation email'
		response = {
			"user": email,
			"sent": email_status
		}
		return Response(response, status=status.HTTP_200_OK)

class ProfileViewSet(viewsets.ModelViewSet):
	queryset = UserStatus.objects.all()
	serializer_class = ProfileSerializer

class MyUserViewSet(viewsets.ModelViewSet):
	queryset = UserStatus.objects.all()
	serializer_class = UserStatusSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('watch',)
	@detail_route(methods=['get'])
	def set_watch(self, request, pk=None):
		message = ''
		if 'watch' not in request.query_params:
			return Response({'message': 'watch field is required'}, status=400)
		watch = request.query_params.get('watch')
		userStatus = None
		try:
			userStatus = UserStatus.objects.get(pk=pk)
			original_watch = 0
			if int(watch) == 0:
				original_watch = userStatus.watch
			userStatus.watch = watch
			userStatus.save()
			if int(watch) == 0:
				watch = original_watch
			stream = Stream.objects.get(id=watch)
			watch_count = UserStatus.objects.filter(watch=watch).count()
			stream.watch_count = watch_count
			stream.save()
		except ObjectDoesNotExist:
			return Response({'message': 'User does not exist'}, status=400)
		return Response(self.get_serializer(userStatus).data)
	@detail_route(methods=['get'])
	def set_photo(self, request, pk=None):
		message = ''
		if 'avatar' not in request.query_params:
			return Response({'message': 'avatar field is required'}, status=400)
		avatar = request.query_params.get('avatar')
		userStatus = None
		try:
			userStatus = UserStatus.objects.get(pk=pk)
			userStatus.avatar = avatar
			userStatus.save()
		except ObjectDoesNotExist:
			return Response({'message': 'User does not exist'}, status=400)
		return Response(self.get_serializer(userStatus).data)
	@detail_route(methods=['get'])
	def profile(self, request, pk=None):
		if pk is None:
			return Response({'stream_count': 0, 'leader_count' : 0, "follower_count" : 0, "follow_state" : 0})
		stream_count = self.get_object().streams
		leaders = Follow.objects.filter(leader=pk)
		leader_count = leaders.count()
		follower_count = Follow.objects.filter(follower=pk).count()
		if 'user_id' not in request.query_params:
			return Response({'stream_count': stream_count, 'leader_count' : leader_count, "follower_count" : follower_count, "follow_state" : False})
		user_id = request.query_params.get('user_id')
		follow_state = 0
		for leader in leaders:
			if leader.follower.id == int(user_id) :
				follow_state = leader.id
		return Response({'stream_count': stream_count, 'leader_count' : leader_count, "follower_count" : follower_count, "follow_state" : follow_state})

	@list_route(methods=['post'])
	def register(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		school = request.POST.get('school')

		if not username or not password:
			message = 'invalid parameters'
			return Response({'message': message}, status=101)

		users = User.objects.filter(username = username)
		if users.count() > 0:
			message = 'Username must be unique'
			return Response({'message': message}, status=102)
		user = User()
		user.username = username
		user.email = email
		user.password = password
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		userStatus = UserStatus()
		userStatus.id=user.id
		userStatus.user=user
		userStatus.first_name = first_name
		userStatus.last_name = last_name
		userStatus.school = school
		userStatus.save()
		user.set_password(password)
		return Response({'message': 'successfully'}, status=200)

class FetchTokenView(CsrfExemptMixin, View):
	"""
	Fetch Token View
	"""
	def post(self, request):
		grant_type = request.POST.get('grant_type')
		if grant_type == 'password':
			username = request.POST.get('username')
			password = request.POST.get('password')

			if not username or not password:
				return HttpResponseBadRequest(
					json.dumps({'error': 'username and password required'}),
					content_type='application/json'
					)
			user = get_object_or_404(User, username=username)
			res = authenticate(username=username, password=password)
			if res is None:
				 response = HttpResponse(
					json.dumps({'error': 'invalid username and/or password'}),
					content_type='application/json',
					)
				 response.status_code = 401
				 return response
			if not user.user.is_active:
				response = HttpResponse(
					json.dumps({'error': 'User is inactive'}),
					content_type='application/json',
					)
				response.status_code = 401
				return response
		token_view = TokenView.as_view()
		return token_view(request)
class PasswordResetView(View):
	"""
	Password Reset
	"""
	def get(self, request, uid, token):
		try:
			pk = decode_uid(uid)
		except:
			return render(request, 'djangorestangularjsboilerplate/password-reset/invalid-token.html')
		user = get_object_or_404(User, pk=pk)
		if not default_token_generator.check_token(user, token):
			return render(request, 'djangorestangularjsboilerplate/password-reset/invalid-token.html')
		template_values = {
			'uid': uid,
			'token': token
		}
		return render(request,
			'djangorestangularjsboilerplate/password-reset/password-reset.html',
			template_values
			)
class ForgotPasswordView(View):
	"""
	Forgot Password
	"""
	def post(self, request):
		email = request.POST.get('email')
		if not email:
			return HttpResponseBadRequest('Email Required')
		view = DjoserPasswordResetView.as_view()
		return view(request)

class FollowViewSet(viewsets.ModelViewSet):
	queryset = Follow.objects.all()
	serializer_class = FollowSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('follower', 'leader')
	@list_route(methods=['post'])
	def createFollow(self, request):
		# follower_id = request.query_params.get('follower')
		# leader_id = request.query_params.get('leader')
		follower_id = request.POST.get('follower')
		leader_id = request.POST.get('leader')
		follower = get_object_or_404(UserStatus, pk=follower_id)
		leader = get_object_or_404(UserStatus, pk=leader_id)
		follow = Follow(follower = follower, leader = leader)
		follow.enable = True
		follow.save()
		serializer = self.get_serializer(follow)
		return Response(serializer.data, status=201)
	@list_route(methods=['delete'])
	def deleteFollow(self, request):
		follower_id = request.query_params.get('follower')
		leader_id = request.query_params.get('leader')
		# follower_id = request.POST.get('follower')
		# leader_id = request.POST.get('leader')
		follower = get_object_or_404(UserStatus, pk = follower_id)
		leader = get_object_or_404(UserStatus, pk = leader_id)
		objects = Follow.objects.filter(follower = follower_id, leader = leader_id)
		for obj in objects:
			obj.delete()
		return Response(status = 204)

class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().order_by('-like', 'id')
	serializer_class = CommentSerializer

class StreamViewSet(viewsets.ModelViewSet):
	queryset = Stream.objects.all()
	serializer_class = StreamSerializer
	filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
	filter_fields = ('isLive',)
	search_fields = ('streamer__full_name', )

	@list_route(methods=['get'])
	def add_stream(self, request):
		if 'streamer' not in request.query_params:
			message = 'streamer field is required'
			return Response({'message': message}, status = status.HTTP_400_BAD_REQUEST)
		if 'streamUrl' not in request.query_params:
			message = 'streamUrl field is required'
			return Response({'message': message}, status = status.HTTP_400_BAD_REQUEST)
		streamer_id = request.query_params.get('streamer')
		streamUrl = request.query_params.get('streamUrl')
		streams = Stream.objects.filter(streamer__id = streamer_id)
		streams.delete()
		stream = Stream()
		streamer = get_object_or_404(UserStatus, pk=streamer_id)
		streamer.streams = streamer.streams + 1
		streamer.save();
		stream.streamer = streamer
		stream.streamUrl = streamUrl
		stream.isLive = True
		stream.save();
		return Response(StreamSerializer(stream).data)

class APNSDeviceViewSet(viewsets.ModelViewSet):
	# permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly)
	queryset = APNSDevice.objects.all()
	serializer_class = APNSDeviceSerializer
	@list_route(methods = ['post'])
	def add(self, request):
		registration_id = request.POST.get('registration_id')
		user = request.POST.get('user')
		devices = APNSDevice.objects.filter(registration_id = registration_id).filter(user__id = user)
		for device in devices:
			device.delete()
		device = APNSDevice()
		device.User = User.objects.get(user)
		device.registration_id = registration_id
		device.save()
class UploadList(viewsets.ModelViewSet):
	queryset = AvatarForm.objects.all()
	serializer_class = AvatarSerializer
