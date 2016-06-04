from core.api.ChangeUsers import ChangeApi
from core.reg import Login_logout
from core.reg.Reg_child import Reg
from core.api.ApiReg import AddChildApi,RegApi
from core.socket import socket_controller

from rest_framework.authtoken import views as views_token


__author__ = 'dima'
from django.conf.urls import url
from core import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [


    # socket
    url(r'^socket/new/$', socket_controller.getWs),
    url(r'^socket/$', views.wsPage),
    # handler forms
    url(r'^signin/$', Login_logout.login_logout.login_form),
    url(r'^signup/$', Login_logout.login_logout.reg_form),
    url(r'^add/child/$', Reg.reg_child_form),

    # handler api
    url(r'^api/signup/$', RegApi.as_view()),
    url(r'^api/add/child/$', AddChildApi.as_view()),
    url(r'^api/edit/$', ChangeApi.as_view()),

    #utils for log
    url(r'^api/get-token/$', views_token.obtain_auth_token),

]

urlpatterns = format_suffix_patterns(urlpatterns)