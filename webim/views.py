#!/usr/bin/env python
#coding: utf-8

import time
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson
from .plugin import Plugin
from .models import Model
from .client import Client
from .setting import WEBIM_CONFIG

# Create your views here.

def current_user(request):
    '''
    Demo User
    '''
    return {'id': '1', 'nick': 'user1', 
            'show': 'available', 
            'avatar': 'static/webim/images/male.png'}

def current_uid(request):
    return current_user(request)['id']

def current_client(request):
    ticket = ''
    if 'ticket' in request.GET:
        ticket = request.GET['ticket']
    if 'ticket' in request.POST:
        ticket = request.POST['ticket']
    return Client(current_user(request), WEBIM_CONFIG['domain'], WEBIM_CONFIG['apikey'], ticket=ticket, host=WEBIM_CONFIG['host'], port=WEBIM_CONFIG['port'])

def index(request):
    return HttpResponse("ok")

def boot(request):
    response = HttpResponse(render(request, 'webim/boot.js'))
    response['Content-Type'] = 'text/javascript'
    return response

def online(request):
    uid = current_uid(request)
    client = current_client(request)

    buddies = Plugin.buddies(uid)
    rooms = Plugin.rooms(uid)

    buddy_ids = [buddy['id'] for buddy in buddies]
    room_ids = [room['id'] for room in rooms]

    data = client.online(buddy_ids, room_ids)

    presences = data['presences']

    for buddy in buddies:
        if buddy['id'] in presences:
            buddy['presence'] = 'online'
            buddy['show'] = presences[buddy['id']]

    data['buddies'] = buddies
    data['rooms'] = rooms
    data['server_time'] = time.time()*1000
    data['user'] = current_user(request)
    return JsonResponse(data)

def offline(request):
    current_client(request).offline()
    return JsonResponse('ok')

def refresh(request):
    current_client(request).offline()
    return JsonResponse('ok')

def message(request):
    user = current_user(request)
    type = request.POST['type']
    offline = request.POST['offline']
    to = request.POST['to']
    body = request.POST['body']
    style = ''
    if 'style' in request.POST:
        style = request.POST['style']
    send = 0 if offline == 'true' else 1
    timestamp = time.time() * 1000
    message = {
        'to':   to,
        'type': type,
        'body': body,
        'style': style,
        'timestamp': timestamp
    }
    if send == 1:
        current_client(request).message(message) 
    if not body.startswith('webim-event:'): 
        message.update({
            'send': send,
            'from': user['id'],
            'nick': user['nick']
        })
        Model.insert_history(message)
    return JsonResponse('ok')

def presence(request):
    show = request.POST['show']
    status = request.POST['status']
    current_client(request).presence({
        'show': show, 
        'status': status
    })
    return JsonResponse('ok')

def status(request):
    to = request.POST['to']
    show = request.POST['show']
    current_client(request).status({'to': to, 'show': show})
    return JsonResponse('ok')

def setting(request):
    data = request.POST['data']
    Model.setting(current_uid(request), data)
    return JsonResponse('ok')

def history(request):
    uid = current_uid(request)
    to = request.GET['id']
    type = request.GET['type']
    histories = Model.histories(uid, to, type)
    return JsonResponse(histories)

def clear_history(request):
    Model.clear_histories(current_uid(request), request.POST['id'])
    return JsonResponse('ok')

def download_history(request):
    to = request.GET['id']
    type = request.GET['type'] 
    Model.histories(current_uid(request), to, type, 100)
    response = HttpResponse(render(request, 'webim/download_history.html', histories=histories))
    response['Content-Type'] = 'text/html;charset=utf-8'
    response['Content-Disposition'] = "attachment; filename=\"histories-%d.html\"" % time.time()
    return response

def chatbox(request):
    to = request.GET['id']
    response = HttpResponse(render(request, 'webim/chatbox.html'))
    return response

def invite(request):
    uid = current_uid(request)
    client = current_client(request)
    roomid = request.POST['id']
    nick = request.POST['nick']
    if(len(nick) == 0):
        return errorReply(400, 'Bad Request')
    room = Model.find_room(roomid)
    if(room is None):
        room = Model.create_room({
            'owner': current_uid(request),        
            'name': roomid, 
            'nick': nick
        })
    Model.join_room(roomid, uid, nick) 
    member_ids = request.POST['members'].split(',')
    members = Plugin.buddies_by_ids(uid, member_ids)
    Model.invite_members(roomid, members)
    for m in members:
        body = "webim-event:invite|,|%s|,|%s" % (roomid, nick)
        client.message({
            'type': 'chat',
            'to': m['id'],
            'body': body,
            'style': '',
            'timestamp': time.time()*1000
        })
    client.join(roomid)
    return JsonResponse({
        'id': room['name'],
        'nick': room['nick'],
        'temporary': True,
        'avatar': 'static/webim/images/room.png'
    })

def join(request):
    roomid = request.POST['id']
    nick = request.POST['nick']
    room = Plugin.find_room(roomid)
    if(room is None):
        room = Model.find_room(roomid)
    if(room is None):
        return errorReply(404, 'Cannot find room: ' + roomid)
    Model.join_room(roomid, current_uid(request), nick)
    current_client(request).join(roomid)
    return JsonResponse({
        'id': roomdid,
        'nick': nick,
        'temporary': true,
        'avatar': '#'
    })

def leave(request):
    roomid = request.POST['id']
    current_client(request).leave(room)
    Model.leave_room(room, current_uid(request))
    return JsonResponse('ok')

def members(request):
    members = []
    roomid = request.GET['id']
    room = Plugin.find_room(roomid)
    if(room is not None):
        members = Plugin.members(roomid)
    else:
        room = Model.find_room(roomid)
        if(room is not None):
            members = Model.members(roomid)
    if(room is None):
        return HttpResponse("Cannot found room: " + roomid)
    presences = current_client(request).members(roomid)
    for m in members:
        if(m['id'] in presences):
            m['presence'] = 'online'
            m['show'] = presences[m['id']]
        else:
            m['presence'] = 'offline'
            m['show'] = 'unavailable'
    return JsonResponse(members)

def block(request):
    room = request.POST['id']
    Model.block(room, current_uid(request))
    return JsonResponse('ok')

def unblock(request):
    room = request.POST['id']
    Model.unblock(room, current_uid(request))
    return JsonResponse('ok')

def notifications(request):
    uid = current_uid(request)
    return JsonResponse(Plugin.notifications(uid))

def upload(request):
    return JsonResponse('ok')

#private methods
#......
#
def JsonResponse(data):
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")



