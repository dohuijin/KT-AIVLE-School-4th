# boards/urls.py
from django.urls import path
from .views import *
from . import views
# from .views import library_view

# app_name = 'boards'

urlpatterns = [
    path('post/', post_list, name='post_list'),
    path('', post_list, name='post_list'),
    path('create/', create_post, name='create_post'),
    path('post_upload/', views.post_upload, name='post_upload'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('board/', post_list, name='Board'),
    path('add_comment/<int:post_id>', add_comment, name='add_comment'),
    path('comment_detail', comment_detail, name='comment_detail'),
    path('delete_comment', delete_comment, name='delete_comment'),
]