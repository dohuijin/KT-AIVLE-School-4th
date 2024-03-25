from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import check_duplicate_username


app_name = 'login'
urlpatterns=[
    path("login/",auth_views.LoginView.as_view(),name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('check_duplicate_username/', check_duplicate_username, name='check_duplicate_username'),
    
]
