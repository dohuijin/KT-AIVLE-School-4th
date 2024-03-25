from django.db import models
import os


class CameraImage(models.Model):
    image = models.ImageField(upload_to="webcam_image/")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=True)
    
    def delete(self, *args, **kwargs):
        # 파일 시스템에서 이미지 삭제
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)
        # 모델 레코드 삭제
        self.is_deleted = False
        self.save()
        super().delete(*args, **kwargs)