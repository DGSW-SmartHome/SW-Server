from django.shortcuts import render
from rest_framework.views import APIView
from .services.returnStatusCode import *

from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import *


@method_decorator(csrf_exempt, name='dispatch')
class signUp(APIView):
    def post(self, request):
        try:
            id = request.data['id']
            username = request.data['username']
            password = request.data['password']
        except (KeyError, ValueError):
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            User.objects.get(id=id)
        except ObjectDoesNotExist:
            userModel = User.objects.create_user(
                password=password,
                id=id,
                username=username
            )
            userModel.save()
            try:
                token = Token.objects.create(user=userModel)
            except IntegrityError:
                token = Token.objects.get(user=userModel)
            return JsonResponse(OK_200(data={"token": token.key}), status=200)
        return JsonResponse(BAD_REQUEST_400(data={}, message='User Already Exists'))


@method_decorator(csrf_exempt, name='dispatch')
class signIn(APIView):
    def post(self, request):
        try:
            user = authenticate(id=request.data['id'], password=request.data['password'])
        except (KeyError, ValueError):
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        if user is not None:
            try:
                token = Token.objects.create(user=user)
            except IntegrityError:
                token = Token.objects.get(user=user)
            return JsonResponse(OK_200(data={"token": token.key}), status=200)
        return JsonResponse(BAD_REQUEST_400(message='Invalid value', data={}), status=400)


@method_decorator(csrf_exempt, name='dispatch')
class checkTokenValidation(APIView):
    def get(self, request):
        userModel = request.user
        return JsonResponse(CUSTOM_CODE(status=200, data={}, message='Valid Token'), status=200)




# id username password