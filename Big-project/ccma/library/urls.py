# library/urls.py
from django.urls import path
from .views import *

app_name = 'library'

urlpatterns = [
    path('', index, name='library'),
    path('music-list/', music_list, name='music_list'),
    path('delete_music/<int:music_id>/', delete_music, name='delete_music'),
    path('delete_video/<int:video_id>/', delete_video, name='delete_video'),
    path('edit_music_name', edit_music_name, name='edit_music_name'),
    path('edit_video_name', edit_video_name, name='edit_video_name'),
]