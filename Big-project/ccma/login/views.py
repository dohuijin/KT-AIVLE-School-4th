# views.py
from django.shortcuts import render, redirect
from .forms import SignUpForm  # 수정: 올바른 SignUpForm을 import
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # 수정: UserCreationForm 대신 SignUpForm 사용
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = SignUpForm()  # 수정: UserCreationForm 대신 SignUpForm 사용
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                form.add_error('password', 'Invalid username or password')  # 특정 필드에 에러 메시지 추가
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def check_duplicate_username(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)

        if username is not None:
            try:
                user = CustomUser.objects.get(username=username)
                return JsonResponse({'is_taken': True})
            except CustomUser.DoesNotExist:
                return JsonResponse({'is_taken': False})

    return JsonResponse({'error': 'Invalid request'})
