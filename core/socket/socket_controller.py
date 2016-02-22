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
                    checker.handler_socket(json.loads(i.decode('utf-8')),request)
                except json.JSONDecodeError:
                    pass
        except AttributeError:
            pass
        finally:
                pass

    print(request)
    # # worked code
    # if request.user.is_anonymous():
    #     return HttpResponseRedirect('/whereiam/signin/')
    #
    # user_request = request.user
    #
    # # list of all requests
    # common_request = []
    #
    # common_request.append({str(request.user):request})
    #
    # # list of all people
    # # children and parent
    # common_people = []
    #
    #
    #
    # try:
    #     # get children
    #     children = user_request.parent.child.all()
    #     common_people.extend(children)
    # except:
    #     # get parent related children
    #     parent_child = user_request.children.parent_set.all()
    #     children = user_request.children.parent_set.get().child.all()
    #     common_people.extend(parent_child)
    #     common_people.extend(children)
    #
    #
    # for i in common_request:
    #     print(common_people)
    #
    #     # User.objects.get(username="child1").children.parent_set.all()
    #
    # print(client)


    # if request.user.
    # if request.is_websocket:
    #
    #     try:
    #         for i in request.websocket:
    #
    #             parse_request= json.loads(i.decode('utf-8'))
    #             print(parse_request)
    #             method_change.post(parse_request,request)
    #
    #     except AttributeError:
    #         pass
    #
    #
    #     finally:
    #             pass
