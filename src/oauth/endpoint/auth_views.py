from django.shortcuts import render
import requests
# rom google.auth.transport import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from ..services import google, spotify, vk
from .. import serializer


def google_login(request):
    """Google Login"""
    return render(request, 'oauth/google_login.html')

def spotify_login(request):
    """Spotify Login"""
    return render(request, 'oauth/spotify_login.html')

def vk_login(request):
    """vk Login"""
    return render(request, 'oauth/vk_login.html')

@api_view(['POST'])
def google_auth(request):
    """Подтвeрждение входа в Google"""
    google_data = serializer.GoogleAuth(data=request.data)

    if google_data.is_valid():
        token = google.check_google_auth(google_data.data)
        return Response(token)
    else:
        return AuthenticationFailed(code=403, detail='Bad data Google')

@api_view(['GET'])
def spotify_auth(request):
    """Подтвeрждение входа в Spotify"""
    #print(request.query_params)
    token = spotify.spotify_auth(request.query_params.get('code'))
    return Response(token)

@api_view(['GET'])
def vk_auth(request, *args, **kwargs):
    """Подтвeрждение входа в VK"""
    token = vk.vk_auth(request.query_params.get('code'))
    return Response(token)
