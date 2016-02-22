# coding:utf-8
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from dwebsocket import accept_websocket, require_websocket
from rest_framework import serializers
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
#
# from dwebsocket.decorators import accept_websocket, require_websocket
#
#
from core import Listener
from core.forms import Login, Reg
from core.models import Parent, Children
from core.serializers import SnippetSerializerParent, SnippetSerializerChildren



def wsPage(request):
       pass
