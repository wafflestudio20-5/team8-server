from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.shortcuts import render
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter

from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import SocialLoginView

# Create your views here.
BASE_URL = 'http://localhost:8000/api/v1/accounts/rest-auth/'
KAKAO_CALLBACK_URI = BASE_URL + 'kakao/callback/'
NAVER_CALLBACK_URI = BASE_URL + 'naver/callback/'
GOOGLE_CALLBACK_URI = BASE_URL + 'google/callback/'
GITHUB_CALLBACK_URI = BASE_URL + 'github/callback/'


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callbakc_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer


class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    callback_url = NAVER_CALLBACK_URI
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URI
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer