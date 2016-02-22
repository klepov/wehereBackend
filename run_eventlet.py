__author__ = 'dima'
from eventlet import wsgi, patcher
patcher.monkey_patch()

import sys
import getopt
import eventlet
from core.wsgi import application


addr, port = '192.168.1.33', 8000
opts, _ = getopt.getopt(sys.argv[1:], "b:")
for opt, value in opts:
    if opt == '-b':
        addr, port = value.split(":")

wsgi.server(eventlet.listen((addr, int(port))), application)