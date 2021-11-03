from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.fineDustInfo)
admin.site.register(models.weatherInfo)
admin.site.register(models.userRoomLight)
admin.site.register(models.userRoomPlug)
