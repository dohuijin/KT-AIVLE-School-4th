# main/urls.py
from django.urls import path
from .views import index, result
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from .views import *

app_name = 'main'

urlpatterns = [
    path('result/', result, name='result'),
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('login/',include('login.urls')),
    path('boards/', include('boards.urls')),
    path('', index_view, name='index'),
    path('edit_audio', edit_audio, name='edit_audio'),
    path('edit_title/',edit_title, name = 'edit_title'),
    path('meeting_gen/', meeting_gen, name = 'meeting_gen'),
    path('meeting_result/', meeting_result , name = 'meeting_result'),
]