import json

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from dwebsocket import accept_websocket

from core.models import Children, Parent
from core.socket.Checker import Check

checker = Check()
@accept_websocket
def getWs(request):

    if request.is_websocket:
        try:
            for i in request.websocket:
                try:
                    print(json.loads(i.decode('utf-8')))
                    checker.handler_socket(json.loads(i.decode('utf-8')),request)
                except json.JSONDecodeError:
                    pass
        except AttributeError:
            checker.user_leave(request)
        finally:
                pass

    print(request)
