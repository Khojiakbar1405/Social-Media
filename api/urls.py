from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.UserAPIView.as_view()),
    path('user-relation/', views.UserRelationAPIView.as_view()),
    path('chat/', views.UserAPIView.as_view()),
    path('massage/', views.UserAPIView.as_view()),
    path('following/<int:pk>/', views.following),
    path('follower/<int:pk>/', views.follower),
    path('post', views.PostView.as_view()),
    path('post/<int:id>', views.PostView.as_view()),
    path('filter', views.filter_post),
    path('comment/<int:id>', views.CommentView.as_view()),
]