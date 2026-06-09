import json
import secrets
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def google_oauth_enabled():
    return bool(
        getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '')
        and getattr(settings, 'GOOGLE_OAUTH_CLIENT_SECRET', '')
    )


def google_redirect_uri(request):
    path = '/accounts/google/callback/'
    if request:
        return request.build_absolute_uri(path)
    base = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000').rstrip('/')
    return f"{base}{path}"


def build_google_auth_url(request):
    state = secrets.token_urlsafe(32)
    request.session['google_oauth_state'] = state
    params = urllib.parse.urlencode({
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'redirect_uri': google_redirect_uri(request),
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'online',
        'prompt': 'select_account',
        'state': state,
    })
    return f"{GOOGLE_AUTH_URL}?{params}"


def _post_form(url, data):
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=encoded, method='POST')
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def _get_json(url, access_token):
    req = urllib.request.Request(
        url,
        headers={'Authorization': f'Bearer {access_token}'},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def fetch_google_profile(code, request):
    token_payload = _post_form(GOOGLE_TOKEN_URL, {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
        'redirect_uri': google_redirect_uri(request),
        'grant_type': 'authorization_code',
    })
    access_token = token_payload.get('access_token')
    if not access_token:
        raise ValueError("Token Google invalide.")
    return _get_json(GOOGLE_USERINFO_URL, access_token)


def get_or_create_google_user(profile):
    email = (profile.get('email') or '').lower().strip()
    if not email:
        raise ValueError("Email Google non disponible.")
    if not profile.get('email_verified', True):
        raise ValueError("Email Google non vérifié.")

    prenom = profile.get('given_name') or profile.get('name', '').split(' ')[0] or 'Utilisateur'
    nom = profile.get('family_name') or 'Google'
    google_sub = profile.get('sub') or secrets.token_hex(8)

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'prenom': prenom[:100],
            'nom': nom[:100],
            'telephone': f'google-{google_sub}'[:100],
            'filiere': 'GL',
            'niveau': 'L1',
            'is_active': True,
        },
    )
    if created:
        user.set_unusable_password()
        user.save()
    elif not user.is_active:
        user.is_active = True
        user.save(update_fields=['is_active'])
    return user, created
