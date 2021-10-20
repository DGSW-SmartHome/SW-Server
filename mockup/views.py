import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpRequest, JsonResponse
from rest_framework.views import APIView
from v1.services.returnStatusCode import *


@method_decorator(csrf_exempt, name='dispatch')
class videos(APIView):
    def get(self, request):
        returnValue = {
            "article": []
        }
        for x in range(1, 1001):
            returnValue["article"].append({
                "name": str(x),
                "video": "https://clips-media-assets2.twitch.tv/AT-cm%7Cu1Z56m2tcVNqU4LxY98dcQ.mp4"
            })
        return JsonResponse(OK_200(data=returnValue), status=200)

