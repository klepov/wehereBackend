from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Parent, Children


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
            # если пароль совпадает и юзера нет в бд то создать его
            if password1 == password2:
                auth = authenticate(username=login, password=password1)
                if auth is None:
                    user = User.objects.create_user(username=login,
                                                    password=password1)
                    user.save()
                    p = Parent(user=user,name = name)

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
                if not User.objects.filter(username=login):
                    password1 = request.data['password1']
                    password2 = request.data['password2']
                    name = request.data['name_child']
                    if password1 == password2:

                        user = User.objects.create_user(username=login,
                                                        password=password1)
                        user.save()

                        children = Children(user=user,name = name)

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