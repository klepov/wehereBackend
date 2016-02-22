from django.http import HttpResponse
from requests import Response


def start(request):
    html = "<html><body><h1 style=font-size:"+"300px"+";text-align:" + "center"+";>SOON...</h1></body></html>"
    return HttpResponse(html)