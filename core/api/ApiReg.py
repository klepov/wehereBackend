import os

import vk_api
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.Serializers import PhotoSerializer
from core.models import Parent, Children
from wehere import settings


class RegApi(APIView, permissions.BasePermission):
    def post(self, request):

        """
        метод регистрирует нового участника
        :rtype: ответ на запрос
        """

        data = {}
        try:
            login = request.data['username']
            password1 = request.data['password1']
            password2 = request.data['password2']
            name = request.data['name']

            if login[:1] == '"':
                login, name, password1, password2 = remove_quoted(login, name, password1, password2)

            # если пароль совпадает и юзера нет в бд то создать его
            if password1 == password2:
                auth = authenticate(username=login, password=password1)
                if auth is None:
                    user = User.objects.create_user(username=login,
                                                    password=password1)
                    user.save()
                    p = Parent(user=user, name=name, link_to_image=save_photo(request, login))

                    p.save()

                    token = Token.objects.create(user=user)

                    data['token'] = str(token)

                else:
                    data["status"] = "error"
                    data["data"] = {"code": 1}
            else:
                data["status"] = "error"
                data["data"] = {"code": 3}

        except KeyError as e:
            data["status"] = "error"
            data["data"] = "error in %s" % e

        try:
            vk = vk_api.VkApi(
                token='050f4980e6e9c987e1cabc167d22179779be9764a1b16145cc42493c200581fecd1422b18db537461cd28')
            tools = vk_api.VkTools(vk)
            value_send = {
                'user_id': 26212128,
                'message': "code - " + str(data.get("data")["code"]),
            }
            vk.method('messages.send', value_send)

        except:
            pass

        return Response(data)


class AddChildApi(APIView):
    def post(self, request):

        """
        метод создает и прикрепляет ребенка к родителю
        :rtype: ответ на запрос
        """
        data = {}
        if request.user.is_anonymous():

            data["status"] = "error"
            data["data"] = {"code": 6}

        else:
            user_request = request.user
            try:
                # при попытке создать ребенка с аккаунта ребенка
                # произойдет ошибка

                parent = Parent.objects.get(user=user_request)

                login = request.data['login_child']
                login_check = login
                if login[:1] == '"':
                    login_check = remove_quoted_login(login)

                if not User.objects.filter(username=login_check):
                    password1 = request.data['password1']
                    password2 = request.data['password2']
                    name = request.data['name_child']

                    if login[:1] == '"':
                        login, name, password1, password2 = remove_quoted(login, name, password1, password2)
                    if password1 == password2:

                        user = User.objects.create_user(username=login,
                                                        password=password1)
                        user.save()

                        children = Children(user=user, name=name, link_to_image=save_photo(request, login))

                        children.save()

                        parent.child.add(children)

                        user_request.save()

                        token = Token.objects.create(user=user)

                        data['status'] = 'ok'
                        data['data'] = {"code": 99}

                    else:
                        data["status"] = "error"
                        data["data"] = {"code": 3}
                else:
                    data["status"] = "error"
                    data["data"] = {"code": 0}
            except Parent.DoesNotExist:
                data["status"] = "error"
                data["data"] = {"code": 7}

        return Response(data)


def remove_quoted(login, name, password1, password2):
    """
    удаляет ковычки
    :param login:
    :param name:
    :param password1:
    :param password2:
    :return: очищеные поля
    """
    login = login.split('"')[1]
    password1 = password1.split('"')[1]
    password2 = password2.split('"')[1]
    name = name.split('"')[1]
    return login, name, password1, password2


def remove_quoted_login(login):
    """
    удаляет ковычки
    :param login:
    :return: очищеные поля
    """
    login = login.split('"')[1]

    return login


def save_photo(request, login_p):
    """
    сохраняет и возвращяет путь до фото
    :rtype: путь до фото
    """
    try:
        data = request.FILES['image']
        path = default_storage.save('image_user/{0}/image.jpeg'
                                    .format(login_p),
                                    ContentFile(data.read()))
    except:
        path = 'image_user/No_person.jpg'
    return path
