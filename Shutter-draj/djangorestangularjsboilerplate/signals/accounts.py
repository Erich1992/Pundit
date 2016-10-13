from django.contrib.auth.signals import user_logged_in
from djangorestangularjsboilerplate.models import UserStatus

def check_user_status(sender, user, request, **kwargs):
    status = UserStatus.objects.get(id=user.id)
    print 'user is active? ' + status

user_logged_in.connect(do_stuff)