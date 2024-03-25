from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from .views import test, result


app_name = 'webcam'


urlpatterns = [
    path('', test, name = 'index'),
    path('capture/', test, name='capture'),
    path('result/', result, name='result'),

]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)