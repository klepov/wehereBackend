import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from idna import unicode
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.serializers import SnippetSerializerParent
from core.models import Parent, Children


class Reg_api(APIView, permissions.BasePermission):
    def post(self, request):

        data = {}
        try:
            login = request.data['username']
            password1 = request.data['password1']
            password2 = request.data['password2']
            # если пароль совпадает и юзера нет в бд то создать его
            if password1 == password2:
                auth = authenticate(username=login, password=password1)
                if auth is None:
                    user = User.objects.create_user(username=login,
                                                    password=password1)
                    user.save()
                    p = Parent(user=user)

                    p.save()

                    token = Token.objects.create(user = user)

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

        return Response(data)




class Add_child_api(APIView):

    def post(self, request):


        data = {}
        if request.user.is_anonymous():

            data["status"] = "error"
            data["data"] = {"code": 3}

        else:
            parent_user = request.user
            login = request.data['name_child']
            if not User.objects.filter(username=login):
                password1 = request.data['password1']
                password2 = request.data['password2']

                if password1 == password2:

                    user = User.objects.create_user(username=login,
                                                    password=password1)
                    user.save()

                    children = Children(user=user)

                    children.save()

                    Parent.objects.get(user = parent_user).child.add(children)

                    parent_user.save()


                    data['status'] = 'ok'
                    data['data'] = {"code": 99}

                else:
                    data["status"] = "error"
                    data["data"] = {"code": 3}
            else:
                data["status"] = "error"
                data["data"] = {"code": 0}

        return Response(data)
