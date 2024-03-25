#main/views.py
from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from audiocraft.models import musicgen
from audiocraft.data.audio import audio_write
from django.conf import settings
from django.conf.urls.static import static
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import requests
from moviepy.editor import *
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play
from main.views import music_model, processor, text_model
from datetime import datetime 

try:
    from IPython.display import display as ipd
except ImportError:
    ipd = None  # IPython이 없으면 ipd를 None으로 설정

from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoForm
from .models import *

def edit_video(request,video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'video/edit_video.html', context={'video_object': video})

def index(request):
    if request.method == 'POST':
        print(request.FILES)
        form = VideoForm(request.POST,request.FILES)
        if form.is_valid():
            video = form.save()
            return redirect('video:edit_video', video_id=video.id)
    return render(request, 'video/index.html')

        
def mix_music(background_file, foreground_file, output_file,delay_time,minus_sound):
    # 배경음악 파일 로드
    delay_time*=1000

    background_music = AudioSegment.from_file(background_file)
    # 전경음악 파일 로드
    foreground_music = AudioSegment.from_file(foreground_file)-minus_sound
    print(len(foreground_music),len(background_music))
    # 두 음악 파일의 길이 맞추기
    if len(background_music[delay_time:]) < len(foreground_music):
        foreground_music = foreground_music[:len(background_music[delay_time:])]

    print(len(foreground_music),len(background_music))
    # 두 음악 파일 병렬로 섞기
    mixed_music = background_music[:delay_time]+background_music[delay_time:].overlay(foreground_music)

    # 결과를 새로운 파일로 저장
    mixed_music.export(output_file, format="wav")

def result(request):
    if request.method == 'POST':
        # 이미지 파일을 가져오기
        img_file = request.FILES.get("image")
        set_time= int(request.POST.get("set_time"))
        start_time= float(request.POST.get("start_time"))
        minus_sound=float(request.POST.get("minus_sound"))
        music_type = request.POST.get("music_type")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        music_model.set_generation_params(duration=set_time)
        

        if not img_file:
            return JsonResponse({'error': 'No image file uploaded'})

        # 파일을 PIL Image로 변환
        try:
            raw_image = Image.open(img_file).convert('RGB')
        except Exception as e:
            print(f"Error opening image file: {e}")
            return JsonResponse({'error': 'Error opening image file'})

        # 이미지를 텍스트로 변환
        inputs = processor(raw_image, return_tensors="pt")
        out = text_model.generate(**inputs)
        mood = processor.decode(out[0], skip_special_tokens=True)
        mood += ". and with " + music_type+" music"
        # 텍스트를 사용하여 음악 생성
        res = music_model.generate([mood], progress=True)
        
        # 오디오 파일을 저장할 경로
        audio_file_path = "temp_audio/temp_audio"
        
        audio_write("static/"+audio_file_path, res[0].cpu(), music_model.sample_rate, strategy="loudness")
        
        base_dir = settings.BASE_DIR
        # 동영상 파일과 오디오 파일 경로 설정
        video_file = request.POST.get("video_url")
        video_file = video_file.split(':8000/')[-1]
        audio_file = "static/"+audio_file_path

        # 동영상 로드 추출
        video = VideoFileClip(os.path.join(base_dir,video_file))
        audio_url=f"media/extracted_audio/{timestamp}.wav"
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'media/extracted_audio')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'media/extracted_audio'))
        video.audio.write_audiofile(os.path.join(base_dir,audio_url))

        # 오디오 로드
        background_file = os.path.join(base_dir,audio_url)  # 배경음악 파일
        foreground_file = os.path.join(base_dir,audio_file+'.wav')  # 전경음악 파일
        audio_file = os.path.join(base_dir,"media/mixed_video/mixed_audio.wav")
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'media/mixed_video')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'media/mixed_video'))
        mix_music(background_file, foreground_file, audio_file,start_time,minus_sound)

        audio = AudioFileClip(os.path.join(base_dir,audio_file))


        # 오디오를 동영상에 삽입
        #final_video = video.set_audio(CompositeAudioClip([audio.set_start(0)]))
        final_video = video.set_audio(audio)
        video_url=f"media/mixed_video/edited{timestamp}.mp4"
        # 삽입된 오디오가 있는 동영상 파일로 저장
        final_video.write_videofile(os.path.join(base_dir,video_url))
        
        # 생성된 동영상을 데이터베이스에 저장
        generated_content = EditedVideo.objects.create(username=request.user.username, video_file=f"mixed_video/edited{timestamp}.mp4", user_id=request.user)

        #audio_url = request.build_absolute_uri(static(f'temp_audio/{audio_file_name}'))
        
        #return render(request, 'main/result.html', {'audio_url': audio_file_path+'.wav'})
        return JsonResponse({'video_url': "/"+video_url})
        # 오디오 파일의 URL 생성
        audio_url = request.build_absolute_uri(static(audio_file_path))

    return JsonResponse({'error': 'Invalid request method'})





