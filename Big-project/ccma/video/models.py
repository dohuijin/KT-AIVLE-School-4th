# video_project/models.py

from django.db import models
from django.conf import settings

class Video(models.Model):
    video_file = models.FileField(upload_to='video/')
    
class EditedVideo(models.Model):
    video_name = models.CharField(max_length=255, default='None')
    username = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='mixed_video/')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    models.CharField(max_length=255, default='None')
    
    def __str__(self):
        return f"EditedVideo - {self.id}"