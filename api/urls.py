from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.UserAPIView.as_view),
    path('user-relation/', views.UserRelationAPIView.as_view),
    path('chat/', views.UserAPIView.as_view),
    path('massage/', views.UserAPIView.as_view),
]