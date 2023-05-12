from django.shortcuts import render
from rest_framework import generics, status
from django.utils.decorators import method_decorator
from .pagination import VideosPageNumberPagination
from backend_your_movies import settings
from .models import Video
from .serializers import VideoDetailSerializer, VideoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACH_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# Create your views here.
@method_decorator(cache_page(CACH_TTL), name='dispatch')
class VideosListView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = VideosPageNumberPagination
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def get_queryset(self):
        return Video.objects.order_by('-created_at')    
    

class VideosDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    
class OwnVideosListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VideoSerializer
    pagination_class = VideosPageNumberPagination
    queryset = Video.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        return Video.objects.filter(author=user).order_by('-created_at')