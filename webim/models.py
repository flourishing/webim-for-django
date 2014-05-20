from django.db import models
import datetime

# Create your models here.

class Model(object):
    
    @staticmethod
    def rooms(uid):
        names = [m.room for m in Member.objects.filter(uid=uid)]
        rooms = Room.objects.filter(name__in=names)
        return [{'id': room.name, 
                 'nick': room.nick, 
                 'url': room.url, 
                 'pic_url': 'static/webim/room.png', 
                 'temporary': True
                 } for room in rooms]

    @staticmethod
    def histories(uid, to, type = 'chat'):
        if(type == 'chat'):
            histories = History.objects.raw("SELECT * from webim_histories where type=1 and ((to_uid = %s and from_uid = %s and fromdel != 1) or (from_uid = %s and to_uid = %s and todel != 1)) order by timestamp desc limit 50", [to, uid, to, uid])
        else: #grpchat
            histories = History.objects.filter(type=2, to_uid=to, send=1).order_by('-timestamp')[:50]
        data = [ Model.map_history(h) for h in histories ]
        data.reverse()
        return data

    @staticmethod
    def map_history(h):
        return {'send': h.send,
                'type': 'chat' if h.type == 1 else 'grpchat',
                'from': h.from_uid,
                'to': h.to_uid,
                'body': h.body,
                'nick': h.nick,
                'style': h.style,
                'timestamp': h.timestamp} 


    @staticmethod
    def offline_histories(uid, limit = 50):
        histories = History.objects.filter(to_uid=uid, send__not=1).order_by('-timestamp')[:50]
        data = [ Model.map_history(h) for h in histories ]
        data.reverse()
        return data

    @staticmethod
    def insert_history(message):
        chatype = 1
        if(message['type'] == 'grpchat'): chatype = 2
        history = History(
                send=message['send'],
                type=chatype,
                to_uid=message['to'],
                from_uid=message['from'],
                nick=message['nick'],
                body=message['body'],
                style=message['style'],
                timestamp=message['timestamp'])
        history.save()

    @staticmethod
    def clear_histories(uid, to):
        History.objects.filter(from_uid=uid, to_uid=to).update(fromdel=1)
        History.objects.filter(to_uid=uid, from_uid=to).update(todel=1)
        History.objects.filter(todel=1, fromdel=1).delete()

    @staticmethod
    def offline_readed(uid):
        History.objects.filter(to_uid=uid, send=0).update(send=0)

    @staticmethod
    def setting(uid, data=None):
        if(data is None):
            setting = Model.find_setting(uid)
            if(setting is None): return '{}'
            return setting.data
        else:
            setting = Model.find_setting(uid)
            if(setting is None):
                setting = Setting(uid=uid, data=data)
            else:
                setting.data = data
            setting.save()

    @staticmethod
    def find_setting(uid):
        settings = Setting.objects.filter(uid=uid)
        if(len(settings) > 0): return settings[0]
        return None

    @staticmethod
    def find_room(roomid):
        rooms = Room.objects.filter(name=roomid)
        if(len(rooms) >0): return rooms[0]
        return None

    @staticmethod
    def create_room(data):
        room = Room(owner = data['owner'], name = data['name'], nick = data['nick'])
        room.save()
        return data

    @staticmethod
    def members(roomid):
        members = Member.objects.filter(room=roomid)
        return [{'id': m.uid, 'nick': m.nick} for m in members]

    @staticmethod
    def join_room(roomid, uid, nick):
        member = Member(room=roomid, uid=uid, nick=nick)
        member.save()

    @staticmethod
    def leave_room(roomid, uid):
        Member.objects.filter(room=roomid, uid=uid).delete()

    @staticmethod
    def invite_members(roomid, members):
        for member in members:
            Model.join_room(roomid, member['id'], member['nick'])

    @staticmethod
    def block(roomid, uid):
        Blocked(room=roomid, uid=uid).save()

    @staticmethod
    def unblock(roomid, uid):
        Blocked.objects.filter(room=roomid, uid=uid).delete()

class History(models.Model):
    class Meta: 
        db_table = 'webim_histories'
    send = models.IntegerField()
    type = models.IntegerField(default=1)
    to_uid = models.CharField(max_length=40)
    from_uid = models.CharField(max_length=40)
    nick = models.CharField(max_length=40)
    body = models.TextField()
    style = models.CharField(max_length=100)
    timestamp = models.FloatField()
    todel = models.IntegerField(default=0)
    fromdel = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

class Setting(models.Model):
    class Meta: 
        db_table = 'webim_settings'
    uid = models.CharField(max_length=40)
    data = models.TextField()
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

class Room(models.Model):
    class Meta: 
        db_table = 'webim_rooms'
    owner = models.CharField(max_length=40)
    name  = models.CharField(max_length=40)
    nick = models.CharField(max_length=60)
    topic = models.CharField(max_length=60)
    url = models.CharField(max_length=100)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

class Member(models.Model):
    class Meta: 
        db_table = 'webim_members'
    room = models.CharField(max_length=40)
    nick  = models.CharField(max_length=40)
    uid = models.CharField(max_length=40)
    joined = models.DateTimeField(default=datetime.datetime.now)

class Blocked(models.Model):
    class Meta: 
        db_table = 'webim_blocked'
    room = models.CharField(max_length=40)
    uid = models.CharField(max_length=40)
    blocked = models.DateTimeField(default=datetime.datetime.now)

class Visitor(models.Model):
    class Meta:
        db_table = 'webim_visitors'
    name = models.CharField(max_length=40)
    ipaddr = models.CharField(max_length=60)
    url = models.CharField(max_length=100)
    referer = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created = models.DateTimeField(default=datetime.datetime.now)


