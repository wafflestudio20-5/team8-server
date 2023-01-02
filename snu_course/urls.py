from django.urls import path, include
from . import views

urlpatterns =[
    path('', views.CourseList.as_view()),
 ]