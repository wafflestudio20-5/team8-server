from django.urls import path, include
from . import views

urlpatterns =[
    path('', views.FileListView.as_view()),
    path('<str:name>/', views.FileDetailView.as_view()),
]