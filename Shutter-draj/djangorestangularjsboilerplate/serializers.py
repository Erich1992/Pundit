from push_notifications.models import APNSDevice

from rest_framework import serializers
from .models import Follow
from .models import Comment
from .models import Stream
from .models import UserStatus
from .models import AvatarForm
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class DirectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower')
 
class UserStatusSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    leader = DirectiveSerializer(many = True)
    class Meta:
        model = UserStatus
        fields = ('id', 'user', 'school','description', 'avatar', 'watch', 'first_name', 'last_name', 'full_name', 'streams', 'streamer1', 'isLive', 'leader')
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ('id', 'school','description', 'avatar', 'first_name', 'last_name', 'full_name')

class APNSDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = APNSDevice
        fields = ('user', 'registration_id')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'commenter', 'stream', 'content', 'like')

class StreamSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many = True, read_only = True)
    streamer = UserStatusSerializer(read_only = True)
    class Meta:
        model = Stream
        fields = ('id', 'streamer', 'streamUrl', 'comments', 'isLive', 'watch_count');

class FollowSerializer(serializers.ModelSerializer):
    leader = UserStatusSerializer(read_only = True)
    follower = UserStatusSerializer(read_only = True)
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'leader', 'enable')
class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvatarForm
        fields = ('image', )

# class  LikeSerializer(serializers.ModelSerializer):
#     liker = UserStatusSerializer(read_only = True)
#     class Meta:
#         model = Like
#         fields = ('id', 'comment', 'liker')
