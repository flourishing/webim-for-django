#!/usr/bin/env python
#coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson

# Create your views here.

def index(request):
    return HttpResponse("ok")

def boot(request):
    return jsonReply({'abc': u'你好'})

def online(request):
    return 'ok'

def offline(request):
    return 'ok'

def refresh(request):
    return 'ok'

def message(request):
    return 'ok'

def presence(request):
    return 'ok'

def status(request):
    return 'ok'

def setting(request):
    return 'ok'

def history(request):
    return 'ok'

def clear_history(request):
    return 'ok'

def download_history(request):
    return 'ok'

def invite(request):
    return 'ok'

def join(request):
    return 'ok'

def leave(request):
    return 'ok'

def block(request):
    return 'ok'

def unblock(request):
    return 'ok'

def members(request):
    return 'ok'

def notifications(request):
    return 'ok'

def upload(request):
    return 'ok'

def jsonReply(data):
    return HttpResponse(simplejson.dumps(data), content_type="application/json")



