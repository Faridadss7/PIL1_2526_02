from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def email_configure():
    return bool(getattr(settings, 'EMAIL_HOST_USER', ''))


def _site_url(request):
    if request:
        return request.build_absolute_uri('/').rstrip('/')
    return getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000').rstrip('/')


def build_activation_link(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    path = reverse('confirmer_email', kwargs={'uidb64': uid, 'token': token})
    if request:
        return request.build_absolute_uri(path)
    return f"{_site_url(request)}{path}"


def send_activation_email(request, user):
    link = build_activation_link(request, user)
    subject = render_to_string('account/email/activation_subject.txt', {
        'user': user,
    }).strip()
    message = render_to_string('account/email/activation_email.txt', {
        'user': user,
        'activation_link': link,
    })
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
