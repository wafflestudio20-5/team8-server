from django.urls import path, include
from . import views

urlpatterns =[
    path('', views.FileListView.as_view()),
    path('<str:name>/', views.FileDetailView.as_view()),
    path('image/<str:name>/', views.ImageDetailView.as_view()),
]