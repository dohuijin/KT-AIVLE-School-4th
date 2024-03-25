# boards/views.py
from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from library.models import GeneratedContent,EditedVideo
from django.core.serializers import serialize
def create_post(request):
    if request.method == 'POST':
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        musicFile = request.POST.get('musicFile')
        filetype,id=musicFile.split()
        print(filetype,id)
        user = request.user
        if filetype=='music':
            music = GeneratedContent.objects.get(id=id)
            Post.objects.create(title=title, content=content, music_id=music, user=user)
        else:
            video = EditedVideo.objects.get(id=id)
            Post.objects.create(title=title, content=content, video_id=video, user=user)
            
        return HttpResponseRedirect(reverse('post_list'))

    return render(request, 'boards/post_list.html', {'posts': Post.objects.all()})

def post_list(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:
        user=request.user
        MusicList=GeneratedContent.objects.filter(user_id=user)
        VideoList=EditedVideo.objects.filter(user_id=user)
        all_len=len(MusicList)+len(VideoList)
        return render(request, 'boards/post_list.html', {'posts': posts, 'MusicList':MusicList,'VideoList':VideoList,'len':all_len})
    else:
        return render(request,'boards/post_list.html', {'posts': posts,'len':0})

def post_upload(request):
    return render(request, 'boards/post_upload.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('post_list')

def add_comment(request, post_id):
    print(post_id)
    post = get_object_or_404(Post, id=post_id)
    print(post)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        content = request.POST.get('content')
        print(content)
        comment = Comment.objects.create(content=content,author=request.user,post=post)
        return JsonResponse({'content': comment.content, 'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),'id':comment.id})
    return JsonResponse({'error': 'Invalid request'})

def comment_detail(request):
    post_id=request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    json_data = serialize('json', comments)
    return JsonResponse(json_data,safe=False)

def delete_comment(request):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment.delete()
    return JsonResponse({'comment_id': request.POST.get('comment_id')})