# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
'''
class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, help_text='Required. Enter your full name.')

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'password1', 'password2')
'''
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요'}))
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': '이름을 입력해주세요'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = '영문+숫자 8자리 이상 입력해주세요'
        self.fields['password2'].widget.attrs['placeholder'] = '비밀번호를 한번 더 입력해주세요'
