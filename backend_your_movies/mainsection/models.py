from django.db import models
from datetime import date
from members.models import User

# Create your models here.
class Video(models.Model):
    created_at = models.DateField(default=date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=200)
    video_file_original = models.FileField(upload_to='videos', max_length=255)
    video_file_480p = models.FileField(upload_to='videos', blank=True, null=True,max_length=255)
    video_file_720p = models.FileField(upload_to='videos', blank=True, null=True,max_length=255)
    video_file_1080p = models.FileField(upload_to='videos',blank=True, null=True, max_length=255)
    thumbnail = models.FileField(upload_to='thumbnails', blank=True, null=True, max_length=255)
