from django.urls import path, include
from . import views

urlpatterns =[
    path('', views.CourseList.as_view()),
    path('<int:rid>/reviews/', views.ReviewListCreateView.as_view()),
 ]