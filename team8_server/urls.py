"""team8_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from snu_student import views
from .views import change_period, confirm, StateDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('snu_student.urls')),
    path('lectures/', include('snu_course.urls')),
    path('files/', include('snu_file.urls')),
    path('interest/', views.InterestCourseAPIView.as_view()),
    path('cart/', views.CartCourseAPIView.as_view()),
    path('pending/', views.PendingListView.as_view()),
    path('registered/', views.RegisteredCourseAPIView.as_view()),
    path('state/', StateDetail.as_view()),
    path('timetable/<int:num>/', views.TimeTableCourseAPIView.as_view()),
    path('cart/<int:num>/', views.TimeTableInsertAPIView.as_view()),
    path('test/period/', change_period),
    path('test/confirm/', confirm),
#    path('media/file/', views.downloadpdf),
]
