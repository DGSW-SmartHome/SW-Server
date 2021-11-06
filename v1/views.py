from django.shortcuts import render
from rest_framework.views import APIView
from .services.returnStatusCode import *

from .services.MQTT.publish import *
from .services.MQTT.subscribe import *

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
            try:
                userModel = User.objects.create_user(
                    password=password,
                    id=id,
                    username=username
                )
                userModel.save()
                for i in range(1, 7):
                    light = userRoomLight(user=userModel, roomID=i)
                    plug = userRoomPlug(user=userModel, roomID=i)
                    light.save()
                    plug.save()
            except (KeyError, ValueError):
                return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
            try:
                token = Token.objects.create(user=userModel)
            except IntegrityError:
                token = Token.objects.get(user=userModel)
            return JsonResponse(OK_200(data={"token": token.key}), status=200)
        return JsonResponse(BAD_REQUEST_400(data={}, message='User Already Exists'), status=400)


@method_decorator(csrf_exempt, name='dispatch')
class signIn(APIView):
    def post(self, request):
        try:
            user = authenticate(id=request.data['id'], password=request.data['password'])
        except (KeyError, ValueError) as E:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing: ' + str(E), data={}), status=400)
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
        if not request.user.is_authenticated or request.user.is_anonymous:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        userModel = request.user
        return JsonResponse(CUSTOM_CODE(status=200, data={}, message='Valid Token'), status=200)

@method_decorator(csrf_exempt, name='dispatch')
class checkUserExists(APIView):
    def post(self, request):
        try:
            id = request.data['id']
        except (KeyError, ValueError) as E:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing' + str(E), data={}), status=400)
        try:
            User.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse(CUSTOM_CODE(message='No Exiting user', status=200, data={}), status=200)
        except (KeyError, ValueError):
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        return JsonResponse(CUSTOM_CODE(message='There is Exiting user', status=400, data={}), status=400)


@method_decorator(csrf_exempt, name='dispatch')
class fineDustInformation(APIView):
    def post(self, request):
        try:
            firstCityName = request.data['firstCityName']
            lastCityName = request.data['lastCityName']
            fineDustValue = request.data['fineDustValue']
            fineDust = request.data['fineDust']
        except (KeyError, ValueError) as E:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing: ' + str(E), data={}), status=400)
        try:
            fineDustDB = fineDustInfo(
                user=request.user,
                firstCityName=firstCityName,
                lastCityName=lastCityName,
                fullCityName=firstCityName+' '+lastCityName,
                fineDustValue=fineDustValue,
                fineDust=fineDust
            )
            fineDustDB.save()
            return JsonResponse(OK_200(data={}), status=200)
        except (KeyError, ValueError):
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        except Exception as E:
            print(E)
        return JsonResponse(CUSTOM_CODE(message='Unknown Internal Server Error Accorded!', status=500, data={}), status=500)


    def get(self, request):
        try:
            fineDustDB = fineDustInfo.objects.get(user=request.user)
            if not fineDustDB.fullCityName:
                return JsonResponse(CUSTOM_CODE(message="There's no exiting value", status=400, data={}), status=400)
        except ObjectDoesNotExist:
            return JsonResponse(CUSTOM_CODE(message="There's no exiting value", status=400, data={}), status=400)
        try:
            return JsonResponse(OK_200(data={
                "firstCityName": fineDustDB.firstCityName,
                "lastCityName": fineDustDB.lastCityName,
                "fullCityName": fineDustDB.fullCityName,
                "fineDustValue": fineDustDB.fineDustValue,
                "fineDust": fineDustDB.fineDust
            }), status=200)
        except Exception as E:
            print(E)
            return JsonResponse(CUSTOM_CODE(message='Unknown Internal Server Error Accorded!', status=500, data={}), status=500)


@method_decorator(csrf_exempt, name='dispatch')
class weatherInformation(APIView):
    def post(self, request):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            city = request.data['city']
            weather = request.data['weather']
            temperature = request.data['temperature']
        except (KeyError, ValueError):
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            weatherObject = weatherInfo(
                user=request.user,
                cityName=city,
                weather=weather,
                temperature=int(temperature)
            )
            weatherObject.save()
            return JsonResponse(OK_200(data={}), status=200)
        except (KeyError, ValueError):
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)

    def get(self, request):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            weatherObject = weatherInfo.objects.get(user=request.user)
            if not weatherObject.cityName:
                return JsonResponse(CUSTOM_CODE(message="There's no exiting value", status=400, data={}), status=400)
        except ObjectDoesNotExist:
            return JsonResponse(CUSTOM_CODE(message="There's no exiting value", status=400, data={}), status=400)
        return JsonResponse(OK_200(data={
            "city": weatherObject.cityName,
            "weather": weatherObject.weather,
            "temperature": weatherObject.temperature
        }),
        status=200)


@method_decorator(csrf_exempt, name='dispatch')
class roomLightAPI(APIView):
    def get(self, request):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        returnValue = {
            "data": []
        }
        try:
            roomLightObject = userRoomLight.objects.filter(user=request.user)
            roomLightObject = list(roomLightObject)
        except ObjectDoesNotExist:
            roomLightObject = []
            for i in range(1, 7):
                light = userRoomLight(user=request.user, roomID=i)
                light.save()
                roomLightObject.append(light)
        for _roomLightObject in roomLightObject:
            roomDict = {"id": _roomLightObject.roomID, "name": _roomLightObject.roomName, "status": _roomLightObject.status}
            returnValue["data"].append(roomDict)
        return JsonResponse(OK_200(data=returnValue), status=200)

    def post(self, request):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            id = request.data['id']
        except (KeyError, ValueError):
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            roomLightObject = userRoomLight.objects.get(user=request.user, roomID=id)
        except ObjectDoesNotExist:
            return JsonResponse(CUSTOM_CODE(message="There's no exiting value", status=400, data={}), status=400)
        roomLightObject.status = not roomLightObject.status
        if roomLightObject.status:
            returnStatus = 3
        else:
            returnStatus = 0
        mqtt = mqtt_publish()
        mqtt.roomLight(returnStatus, roomLightObject.roomID)
        roomLightObject.save()
        return JsonResponse(OK_200(), status=200)


@method_decorator(csrf_exempt, name='dispatch')
class roomLightNameAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            id = request.data['id']
            name = request.data['name']
        except (KeyError, ValueError):
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            roomLightObject = userRoomLight.objects.get(user=request.user, roomID=id)
        except ObjectDoesNotExist:
            for i in range(1, 7):
                light = userRoomLight(user=request.user, roomID=i)
                light.save()
            roomLightObject = userRoomLight.objects.get(user=request.user, roomID=id)
        roomLightObject.roomName = name
        roomLightObject.save()
        return JsonResponse(OK_200(data={}), status=200)


@method_decorator(csrf_exempt, name='dispatch')
class roomPlugAPI(APIView):
    def get(self, request):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        returnValue = {
            "data": []
        }
        try:
            roomPlugAPI = userRoomPlug.objects.filter(user=request.user)
            roomPlugObject = list(roomPlugAPI)
        except ObjectDoesNotExist:
            roomPlugObject = []
            for i in range(1, 7):
                plug = userRoomPlug(user=request.user, roomID=i)
                plug.save()
                roomPlugObject.append(plug)
        for _roomPlugObject in roomPlugObject:
            roomDict = {"id": _roomPlugObject.roomID, "name": _roomPlugObject.roomName, "status": _roomPlugObject.status}
            returnValue["data"].append(roomDict)
        return JsonResponse(OK_200(data=returnValue), status=200)

    def post(self, request):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            id = request.data['id']
        except (KeyError, ValueError):
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            roomPlugObject = userRoomPlug.objects.get(user=request.user, roomID=id)
        except ObjectDoesNotExist:
            return JsonResponse(CUSTOM_CODE(message="There's no exiting value", status=400, data={}), status=400)
        roomPlugObject.status = not roomPlugObject.status
        mqtt = mqtt_publish()
        mqtt.roomPlug(roomPlugObject.status, roomPlugObject.roomID)
        roomPlugObject.save()
        return JsonResponse(OK_200(), status=200)


@method_decorator(csrf_exempt, name='dispatch')
class roomPlugNameAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            id = request.data['id']
            name = request.data['name']
        except (KeyError, ValueError):
            return JsonResponse(BAD_REQUEST_400(message='Some Values are missing', data={}), status=400)
        try:
            roomPlugObject = userRoomPlug.objects.get(user=request.user, roomID=id)
        except ObjectDoesNotExist:
            for i in range(1, 7):
                plug = userRoomPlug(user=request.user, roomID=i)
                plug.save()
            roomPlugObject = userRoomPlug.objects.get(user=request.user, roomID=id)
        roomPlugObject.roomName = name
        roomPlugObject.save()
        return JsonResponse(OK_200(data={}), status=200)



# id username password


# MQTT 통신 Get Method 예시
# @method_decorator(csrf_exempt, name='dispatch')
# class temp(View):
#     def get(self, request):
#         value = recv()
#         returnValue = {
#             "status": -1,
#             "value": value['temp']
#         }
#         return JsonResponse(returnValue)