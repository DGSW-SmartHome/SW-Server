from django.urls import path, include
from . import views

app_name = 'v1'
urlpatterns = [
    path('user/manage/signup/', views.signUp.as_view(), name='index'),
    path('user/manage/signin/', views.signIn.as_view(), name='index'),
    path('user/manage/tokencheck/', views.checkTokenValidation.as_view(), name='index'),
    path('user/manage/signup/checkusername/', views.checkUserExists.as_view(), name='index'),
    path('user/data/finedust/', views.fineDustInformation.as_view(), name='index'),
    path('user/data/weather/', views.weatherInformation.as_view(), name='index'),
    path('user/data/room/light/', views.roomLightAPI.as_view(), name='index'),
    path('user/data/room/light/name/', views.roomLightNameAPI.as_view(), name='index'),
    path('user/data/room/plug/', views.roomPlugAPI.as_view(), name='index'),
    path('user/data/room/plug/name/', views.roomPlugNameAPI.as_view(), name='index'),
]
