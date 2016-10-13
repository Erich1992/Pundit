from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from djangorestangularjsboilerplate import views

from .views import FetchTokenView, ForgotPasswordView, PasswordResetView, APNS_StopView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'user-status', views.UserStatusViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'myuser', views.MyUserViewSet)
router.register(r'follow', views.FollowViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'stream', views.StreamViewSet)
router.register(r'apns', views.APNSDeviceViewSet)
router.register(r'files', views.UploadList)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^list/$', views.list, name='list'),
    url(r'^password-reset/(?P<uid>\w+)/(?P<token>[A-Za-z0-9_-]+)/?$', PasswordResetView.as_view(), name='password-reset'),
    url(r'^forgot-password/?$', TemplateView.as_view(template_name='djangorestangularjsboilerplate/password-reset/forgot-password.html'), name='forgot-password'),
    url(r'^send-reset-email', ForgotPasswordView.as_view(), name='send-reset-email'),
    url(r'^api-apn/stop/(?P<user_id>[0-9]+)/$', APNS_StopView.as_view(), name='stop'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/token/?$', FetchTokenView.as_view(), name='token'),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^djoser-auth/', include('djoser.urls')),
    url('^.*$', views.IndexView.as_view(), name='index'),
]