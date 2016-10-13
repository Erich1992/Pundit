from django.contrib import admin
from djangorestangularjsboilerplate.models import UserStatus
from djangorestangularjsboilerplate.models import Follow
from djangorestangularjsboilerplate.models import Comment
from djangorestangularjsboilerplate.models import Stream
# from djangorestangularjsboilerplate.models import UploadFileForm

# from djangorestangularjsboilerplate.models import Like

class UserStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active','activation_token', 'watch', 'streams', 'full_name')

class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'leader', 'enable')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'commenter', 'stream','content', 'like')

class StreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'streamer', 'streamUrl', 'isLive')

# class UploadFileFormAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'file')

# class LikeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'comment', 'liker')

admin.site.register(UserStatus, UserStatusAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Stream, StreamAdmin)
# admin.site.register(UploadFileForm, UploadFileFormAdmin)

# admin.site.register(Like, LikeAdmin)
