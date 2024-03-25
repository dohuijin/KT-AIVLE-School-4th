# main/admin.py

from django.contrib import admin
from .models import GeneratedContent

@admin.register(GeneratedContent)
class GeneratedContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'audio')