from django.urls import path
from .views import index, result, edit_video
from django.conf import settings
from django.urls import path

app_name = 'video'

urlpatterns = [
    path('result/', result, name='result'),
    path('', index, name='index'),
    path('<int:video_id>/', edit_video, name='edit_video'),
]