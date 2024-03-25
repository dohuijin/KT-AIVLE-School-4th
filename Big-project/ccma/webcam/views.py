from django.shortcuts import render
from .models import CameraImage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from PIL import Image
import os
from django.conf import settings
from datetime import datetime 
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pydub import AudioSegment

from transformers import BlipProcessor, BlipForConditionalGeneration
from audiocraft.models import musicgen
from audiocraft.data.audio import audio_write
from main.views import music_model, processor, text_model

@csrf_exempt
def test(request):
    if request.method == 'POST':
        image = request.FILES.get('camera-image')
        CameraImage.objects.create(image=image)
    images = CameraImage.objects.all()
    latest_image = CameraImage.objects.last()
    context = {
        'images': images, 
        'latest_image' : latest_image
    }
    
    return render(request, 'webcam/camera_view.html', context)





def result(request):
    if request.method == 'POST':
        # 이미지 파일을 가져오기
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        # music_model.set_generation_params(duration=15)
        music_model.set_generation_params(duration=int(request.POST.get("set_time")))
        minus_sound=int(request.POST.get("minus_sound"))
        music_type=request.POST.get("music_type")
            
        latest_image = CameraImage.objects.last()

        if not latest_image:
            return JsonResponse({'error': 'No image file uploaded'})

        # 이미지 파일의 경로 가져오기
        image_path = latest_image.image.path

        # 파일을 PIL Image로 변환
        try:
            with default_storage.open(image_path, 'rb') as file:    
                raw_image = Image.open(file).convert('RGB')
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
        # audio_file_path = "webcam_audio/webcam_audio"
        audio_file_path = f"webcam_audio/webcam_audio_{timestamp}"
        
        
        audio_path = f"{settings.MEDIA_URL}{audio_file_path}.wav"
        # audio_path = f"media/{audio_file_path}.wav"
        image_url = latest_image.image.url
        audio_write("media/"+audio_file_path, res[0].cpu(), music_model.sample_rate, strategy="loudness")
        
        music = AudioSegment.from_file(os.path.join(settings.BASE_DIR,'media',audio_file_path+'.wav'))-minus_sound
        os.remove(os.path.join(settings.BASE_DIR,'media',audio_file_path+'.wav'))
        music.export(os.path.join(settings.BASE_DIR,'media',audio_file_path+'.wav'), format="wav")
        
        
        return render(request, 'webcam/result.html', {'image': image_url, 'text_result': mood, 'audio_url': audio_path})
    return JsonResponse({'error': 'Invalid request method'})
        
    
    