from django.urls import path
from .views import VideosDetailView, VideosListView, OwnVideosListView, OwnVideosDetailView

urlpatterns = [
    path('v1/videos/<int:pk>/', VideosDetailView.as_view()),
    path('v1/videos/', VideosListView.as_view()),
    path('v1/myvideos/', OwnVideosListView.as_view()),
    path('v1/myvideos/<int:pk>', OwnVideosDetailView.as_view())
]