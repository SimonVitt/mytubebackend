from rest_framework import serializers
from .models import Video
from members.models import User
from members.serializers import UserSerializer

class VideoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=80, min_length=4)
    description = serializers.CharField(max_length=200, min_length=4)
    video_file_original = serializers.FileField(write_only=True)
    thumbnail = serializers.FileField(read_only=True)
    author = UserSerializer(read_only=True)
    created_at = serializers.DateField(read_only=True)
    
    class Meta:
        model = Video
        fields = ['title', 'description', 'author', 'video_file_original', 'thumbnail', 'created_at', 'id']
        
class VideoDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=80, min_length=4)
    description = serializers.CharField(max_length=200, min_length=4)
    video_file_480p = serializers.FileField(read_only=True)
    video_file_720p = serializers.FileField(read_only=True)
    video_file_1080p = serializers.FileField(read_only=True)
    thumbnail = serializers.FileField(read_only=True)
    author = UserSerializer(read_only=True)
    created_at = serializers.DateField(read_only=True)
    
    class Meta:
        model = Video
        fields = ['title', 'description', 'author', 'video_file_480p', 'thumbnail', 'id', 'video_file_720p', 'video_file_1080p', 'created_at']
