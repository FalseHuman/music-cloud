import requests
from src.oauth.models import AuthUser
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from src.oauth.services import base_auth

def get_vk_email(code: str):
    url = f'https://oauth.vk.com/access_token?client_id={settings.VK_CLIENT_ID}&client_secret={settings.VK_SECRET}&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fvk-callback&code={code}'
    res = requests.get(url)
    if res.status_code == 200:
        r = res.json()
        return r.get('email')
    else:
        return None

def vk_auth(code: str):
    email = get_vk_email(code)
    if email is not None:
        user, _ = AuthUser.objects.get_or_create(email=email)
        return base_auth.create_token(user.id)
    else:
        raise AuthenticationFailed(code=403, detail='Bad token VK or user not email in profile VK')
