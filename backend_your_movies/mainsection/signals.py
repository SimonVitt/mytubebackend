from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
import os
import django_rq
from .tasks import convert_video, generate_thumbnail
import backend_your_movies.settings as settings
from django.core.cache import cache


@receiver(post_delete, sender=Video)
def delete_file(sender, instance, **kwargs):
    if instance.video_file_original:
        if os.path.isfile(instance.video_file_original.path):
            os.remove(instance.video_file_original.path)
    if instance.video_file_480p:
        if os.path.isfile(instance.video_file_480p.path):
            os.remove(instance.video_file_480p.path)
    if instance.video_file_720p:
        if os.path.isfile(instance.video_file_720p.path):
            os.remove(instance.video_file_720p.path)
    if instance.video_file_1080p:
        if os.path.isfile(instance.video_file_1080p.path):
            os.remove(instance.video_file_1080p.path)
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)
    cache.delete_many(keys=cache.keys('*videos_list*'))
            
@receiver(post_save, sender=Video)
def video_post_safe(sender, instance, created, **kwargs):
    if created:
        source_split = instance.video_file_original.path.split(".", 1)
        thumbnail_name = os.path.basename(source_split[0])
        thumbnail_saved_path = generate_thumbnail(instance.video_file_original.path, thumbnail_name)
        thumbnail_relative_path = os.path.relpath(thumbnail_saved_path, settings.MEDIA_ROOT)
        instance.thumbnail = thumbnail_relative_path
        instance.save(update_fields=['thumbnail'])
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video, instance.video_file_original.path, instance.pk, '480p')
        queue.enqueue(convert_video, instance.video_file_original.path, instance.pk, '720p')
        queue.enqueue(convert_video, instance.video_file_original.path, instance.pk, '1080p')