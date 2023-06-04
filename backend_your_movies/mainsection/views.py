from django.shortcuts import render
from rest_framework import generics, status
from django.utils.decorators import method_decorator

from .permissions import OwnsVideo
from .pagination import VideosPageNumberPagination
from backend_your_movies import settings
from .models import Video
from .serializers import VideoDetailSerializer, VideoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import never_cache
from django.core.cache import cache


CACH_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# Create your views here.

@method_decorator(never_cache, name='dispatch')
class VideosListView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = VideosPageNumberPagination
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def get_queryset(self):
        queryset = cache.get('videos_list')
        if not queryset:
            queryset = Video.objects.order_by('-created_at')
            cache.set('videos_list', queryset, CACH_TTL)
        return queryset
    

class VideosDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
    permission_classes = [IsAuthenticated]
    
    
class OwnVideosListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoSerializer
    pagination_class = VideosPageNumberPagination
    queryset = Video.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        return Video.objects.filter(author=user).order_by('-created_at')
    
class OwnVideosDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
    permission_classes = [IsAuthenticated, OwnsVideo]
