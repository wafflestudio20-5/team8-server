from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns =[
    path('register/', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('refresh/', views.RefreshApiView.as_view()),
    path('current/', views.UserRetrieveUpdateAPIView.as_view()),
    # path('<int:pk>/', views.UserDetail.as_view()),
 ]