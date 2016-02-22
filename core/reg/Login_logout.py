from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.authtoken.models import Token

from core.forms import Reg, Login
from core.models import Parent


class login_logout():

    def reg_form(request):
        if request.POST:
            form = Reg(request.POST)
            if form.is_valid():
                login = form.data['login']
                password1 = form.data['password1']
                password2 = form.data['password2']

                if password1 == password2:
                    auth = authenticate(username=login, password=password1)
                    if auth is None:
                        user = User.objects.create_user(username=login,
                                                        password=password1)
                        user.save()
                        p = Parent(user=user)

                        p.save()

                        Token.objects.create(user = user)
                        return HttpResponseRedirect('/whereiam/signin')
        else:
            form = Reg()

            return render(request, 'reg.html', {'form': form})


    def login_form(request):

        if request.POST:
            form = Login(request.POST)
            if form.is_valid():

                login_field = form.data['login']
                password_field = form.data['password']

                auth = authenticate(username=login_field,
                                    password=password_field)

                if auth is not None:
                    login(request, auth)

                    return HttpResponseRedirect('/whereiam/socket/new')

                return HttpResponseRedirect('/whereiam/signup/')


        else:
            form = Login()

        return render(request, 'login.html', {'form': form})

