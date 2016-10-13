from django.core.urlresolvers import reverse

def soc_auth_email_val_fn(strategy, backend, code):
    url = strategy.build_absolute_uri(reverse('social:complete', args=(strategy.backend_name,))) + '?verification_code=' + code.code
    return url