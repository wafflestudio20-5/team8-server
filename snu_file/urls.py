from django.urls import path, include

from team8_server import settings
from . import views

urlpatterns =[
    path('<str:name>/', views.FileDetailView.as_view()),
]
if settings.DEBUG:
    urlpatterns += [
        path('', views.FileListView.as_view()),
    ]