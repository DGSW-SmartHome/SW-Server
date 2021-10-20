from django.urls import path, include
from . import views

app_name = 'mockup'
urlpatterns = [
    path('video/', views.videos.as_view(), name='index'),
]
