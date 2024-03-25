from django.shortcuts import render
from .models import GeneratedContent,EditedVideo
from django.shortcuts import redirect, get_object_or_404

def index(request):
    if request.user.is_authenticated:
        user=request.user
        MyVideos=EditedVideo.objects.filter(user_id=user)
        MyMusics=GeneratedContent.objects.filter(user_id=user)
        for MyMusic in MyMusics:
            print(MyMusic.username, MyMusic.image, MyMusic.audio)
        return render(request, 'library.html',{'music_list': MyMusics,'video_list':MyVideos})
    else:
        return render(request,'library.html')

def music_list(request):
    music_list = Music.objects.all()
    return render(request, 'library/music_list.html', {'music_list': music_list})

def delete_music(request, music_id):
    music = get_object_or_404(GeneratedContent, id=music_id)
    print(request.user.username,music.user_id.username)
    if request.user.id==music.user_id.id:
        music.delete()
    return redirect('/library')

def delete_video(request, video_id):
    video = get_object_or_404(EditedVideo, id=video_id)
    if request.user.id==video.user_id.id:
        video.delete()
    return redirect('/library')

def edit_music_name(request):
    print(request.POST)
    music_id=request.POST.get('music_id')
    music_name=request.POST.get('music_name')
    GeneratedContent.objects.filter(id=music_id).update(image_name=music_name)
    return redirect('/library')

def edit_video_name(request):
    print(request.POST)
    video_id=request.POST.get('video_id')
    video_name=request.POST.get('video_name')
    EditedVideo.objects.filter(id=video_id).update(video_name=video_name)
    return redirect('/library')