from django.urls import path, include
from . import views

urlpatterns =[
    path('', views.CourseList.as_view()),
    path('<int:id>/reviews/', views.ReviewListCreateView.as_view()),
    path('<int:id>/reviews/<int:rid>/', views.ReviewRetrieveUpdateDestroyView.as_view()),
    path('<int:id>/reviews/<int:rid>/comments/', views.CommentListCreateView.as_view()),
    path('<int:id>/reviews/<int:rid>/comments/<int:cid>/', views.CommentRetrieveUpdateDestroyView.as_view()),
 ]