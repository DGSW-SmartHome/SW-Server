from django.urls import path, include
from . import views

app_name = 'v1'
urlpatterns = [
    path('user/manage/signup/', views.signUp.as_view(), name='index'),
    path('user/manage/signin/', views.signIn.as_view(), name='index'),
    path('user/manage/tokencheck/', views.checkTokenValidation.as_view(), name='index'),
    path('user/manage/signup/checkusername/', views.checkUserExists.as_view(), name='index'),
]
