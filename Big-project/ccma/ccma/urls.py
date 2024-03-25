# ccma/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from .views import PrivacyPolicyView
from main.views import index
from main.views import index_view
from .views import library_view
from django.conf import settings
from django.conf.urls.static import static

def index(request):
    return render(request,'index.html')

urlpatterns = [
    path('main/', include('main.urls')),
    path('', index, name='default_index'),
    path("admin/", admin.site.urls),
    path('login/',include('login.urls')),
    path('admin/', admin.site.urls),
    path('boards/', include('boards.urls')),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('main/', index_view, name='default_index'),
    path('library/', include('library.urls')),
    path('video/', include('video.urls')),
    path('webcam/', include('webcam.urls', namespace='webcam')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)