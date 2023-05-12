import subprocess
import os
import backend_your_movies.settings as settings

def convert_video(source, instance_pk, resolution):
    import django
    django.setup()
    from .models import Video
    instance = Video.objects.get(pk=instance_pk)
    source_split = source.split(".", 1)
    target = source_split[0] + f'_{resolution}.mp4'
    resolutions = {'480p': 'hd480', '720p': 'hd720', '1080p': 'hd1080'}

    cmd = f'"C:/usr/ffmpeg/bin/ffmpeg.exe" -i "{source}" -s {resolutions[resolution]} -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    subprocess.run(cmd)
    video_relative_path = os.path.relpath(target, settings.MEDIA_ROOT)

    update_field = f'video_file_{resolution}'
    setattr(instance, update_field, video_relative_path)
    instance.save(update_fields=[update_field])

    
def generate_thumbnail(source, thumbnail_name):
    i = 1
    target = os.path.join(settings.MEDIA_ROOT, "thumbnails", f"{thumbnail_name}{i:03d}.jpg")
    while os.path.exists(target):
        i += 1
        target = os.path.join(settings.MEDIA_ROOT, "thumbnails", f"{thumbnail_name}{i:03d}.jpg")
    cmd = f'"C:/usr/ffmpeg/bin/ffmpeg.exe" -ss 0 -i {source} -frames:v 1 -q:v 2 -update 1 {target}'
    subprocess.run(cmd)
    return target
