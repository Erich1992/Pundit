from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings as django_settings


def send_activation_email(instance):
    current_site = Site.objects.get_current()
    email = instance.user.email
    domain = current_site.domain
    site_name = current_site.name
    protocol = 'http'
    url = 'api/user-status/'+ str(instance.pk) +'/activate/?token='+ str(instance.activation_token)
    sender = getattr(django_settings, 'DEFAULT_FROM_EMAIL', None)
    email_title = 'Account activation on ' + site_name

    msg_plain = render_to_string('djangorestangularjsboilerplate/email/activation_email.txt', {
        'domain': domain,
        'site_name': site_name,
        'protocol': protocol,
        'url': url
    })

    msg_html = render_to_string('djangorestangularjsboilerplate/email/activation_email.html', {
        'domain': domain,
        'site_name': site_name,
        'protocol': protocol,
        'url': url
    })

    print 'msg_plain: ', msg_plain, 'msg_html', msg_html

    email_status = send_mail(
        email_title,
        msg_plain,
        sender,
        [email],
        html_message=msg_html,
    )

    return email_status
