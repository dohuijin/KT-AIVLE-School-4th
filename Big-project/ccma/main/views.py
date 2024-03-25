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
from django.shortcuts import render
from .models import GeneratedContent
from datetime import datetime 
from googletrans import Translator
from pydub import AudioSegment

try:
    from IPython.display import display as ipd
except ImportError:
    ipd = None  # IPython이 없으면 ipd를 None으로 설정


translator = Translator()


def index(request):
    return render(request, 'main/index.html')


music_model = musicgen.MusicGen.get_pretrained('small')

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
text_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")



def result(request):
    if request.method == 'POST' and request.user.is_authenticated:
        music_model.set_generation_params(duration=int(request.POST.get("set_time")))
        # 현재 시간을 기반으로 파일 이름 생성
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        minus_sound=int(request.POST.get("minus_sound"))
        music_type=request.POST.get("music_type")
        
        # 이미지 파일을 가져오기
        img_file = request.POST.get("image")
        img_file =os.path.join(settings.BASE_DIR, 'media',img_file.split('media/')[-1])
        if not img_file:
            return JsonResponse({'error': 'No image file uploaded'})
        print(img_file)

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
        print(mood)
        # 텍스트를 사용하여 음악 생성
        res = music_model.generate([mood], progress=True)
        
        # 오디오 파일을 저장할 경로
        audio_file_path = f"temp_audio/temp_audio_{timestamp}"
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'media/temp_audio')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'media/temp_audio'))
        # 이미지 파일의 경로
        image_file_path = f"temp_image/temp_image{timestamp}.png"
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'media/temp_image')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'media/temp_image'))

        # 오디오 파일 저장

        audio_write("media/"+audio_file_path, res[0].cpu(), music_model.sample_rate, strategy="loudness")
        
        music = AudioSegment.from_file(os.path.join(settings.BASE_DIR,'media',audio_file_path+'.wav'))-minus_sound
        os.remove(os.path.join(settings.BASE_DIR,'media',audio_file_path+'.wav'))
        music.export(os.path.join(settings.BASE_DIR,'media',audio_file_path+'.wav'), format="wav")
        # 이미지 파일 저장
        image_path = os.path.join(settings.BASE_DIR, "media", image_file_path)
        raw_image.save(image_path, format="PNG")
        
        image_url = f"{settings.STATIC_URL}{image_file_path}"
        
        # 생성된 이미지와 음악을 데이터베이스에 저장
        generated_content = GeneratedContent.objects.create(username=request.user.username, image=f"{image_file_path}", audio=f"{audio_file_path}.wav",user_id=request.user)
        
        
        # 오디오 파일의 URL 생성
        audio_file_name = "temp_audio"
        #audio_url = request.build_absolute_uri(static(f'temp_audio/{audio_file_name}'))
        
        #return render(request, 'main/result.html', {'image': image_file_path, 'text_result': mood, 'audio_url': audio_file_path+'.wav', 'generated_content': generated_content})

        # 오디오 파일의 URL 생성
        audio_url = request.build_absolute_uri(static(audio_file_path))

        return JsonResponse({'text_result': mood, 'audio_url': audio_file_path+'.wav'})

    return JsonResponse({'error': 'Invalid request method'})

def edit_audio(request):
    if request.method=='POST':
        img_file = request.FILES.get("image")
        try:
            raw_image = Image.open(img_file).convert('RGB')
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        except Exception as e:
            print(f"Error opening image file: {e}")
            return JsonResponse({'error': 'Error opening image file'})
        image_file_path = f"temp_image/temp_image{timestamp}.png"
        image_path = os.path.join(settings.BASE_DIR, "media", image_file_path)
        raw_image.save(image_path, format="PNG")
        return render(request,'main/result.html', {'image':image_file_path})
    return JsonResponse({'error': 'Invalid request method'})

def save_audio(audio, sample_rate, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, 'wb') as audio_file:
        # 여기에서 audio를 파일로 저장하는 코드를 추가
        pass


def display_audio(audio, sample_rate):
    if ipd is not None:
        ipd.display(ipd.Audio(audio, rate=sample_rate))

def index_view(request):
    return render(request, 'main/index.html')


# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse

# @login_required(login_url='/login/')  # 로그인이 필요한 경우 로그인 페이지로 리다이렉트
# def result(request):
#     if request.method == 'POST':
#         # 이하 로직은 그대로 유지
#         if request.user.is_authenticated:
#             # 로그인된 사용자에 대한 추가 로직
#             return JsonResponse({'message': 'Logged in user'})

#     # 로그인이 필요한 경우에만 이 부분에 도달하게 됨
#     return JsonResponse({'error': 'Invalid request'})

def edit_title(request):
    if request.method=='POST':
        meeting_title = request.POST.get("meeting_title")
            
        return render(request,'main/meeting.html', {'meeting_title':meeting_title})
    return render(request,'main/meeting.html')
    
def meeting_result(request):
    return render(request, 'main/meeting_result.html')
        

def meeting_gen(request):
    if request.method == 'POST' and request.user.is_authenticated:
        print(request)
        # music_model.set_generation_params(duration=int(request.POST.get("set_time")))
        set_time= int(request.POST.get("set_time"))
        music_model.set_generation_params(duration=set_time)
        # music_model.set_generation_params(duration = 3)
        # 현재 시간을 기반으로 파일 이름 생성
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        

        
        # 이미지 파일을 가져오기
        text = request.POST.get('text')
        if not text:
            return JsonResponse({'error': 'text is not uploaded'})
        
        
        trans = translator.translate(text, dest = 'en')


        mood = trans.text
        print(mood)
        # 텍스트를 사용하여 음악 생성
        res = music_model.generate([mood], progress=True)
        
        # 오디오 파일을 저장할 경로
        audio_file_path = f"temp_audio/temp_audio_{timestamp}"
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'media/temp_audio')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'media/temp_audio'))
        # 이미지 파일의 경로


        # 오디오 파일 저장
        audio_path = os.path.join(settings.BASE_DIR, audio_file_path)
        audio_write("media/"+audio_file_path, res[0].cpu(), music_model.sample_rate, strategy="loudness")
        
        # 오디오 파일의 URL 생성
        audio_file_name = "temp_audio"
        #audio_url = request.build_absolute_uri(static(f'temp_audio/{audio_file_name}'))
        
        #return render(request, 'main/result.html', {'image': image_file_path, 'text_result': mood, 'audio_url': audio_file_path+'.wav', 'generated_content': generated_content})

        # 오디오 파일의 URL 생성
        audio_url = request.build_absolute_uri(static(audio_file_path))

        # return JsonResponse({'text_result': mood, 'audio_url': audio_file_path+'.wav'})
        return JsonResponse({'text_result': mood, 'audio_url': audio_file_path+'.wav'})

    return JsonResponse({'error': 'Invalid request method'})