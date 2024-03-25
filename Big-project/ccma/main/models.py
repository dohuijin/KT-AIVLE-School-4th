# main/models.py

from django.db import models
from django.conf import settings

class GeneratedContent(models.Model):
    username = models.CharField(max_length=255)
    image = models.ImageField(upload_to='temp_image/')
    audio = models.FileField(upload_to='temp_audio/')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    image_name = models.CharField(max_length=255, default='None')
    def __str__(self):
        return f"GeneratedContent - {self.id}"
