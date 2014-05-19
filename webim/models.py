from django.db import models

# Create your models here.

class Model(object):
    
    @staticmethod
    def rooms(uid):
        return []

    @staticmethod
    def histories(uid, to, type):
        return []

    @staticmethod
    def insert_history(message):
        pass

    @staticmethod
    def clear_histories(uid, to):
        pass

    @staticmethod
    def setting(uid, data=None):
        pass
    
    @staticmethod
    def find_room(roomid):
        return None

    @staticmethod
    def create_room(data):
        pass

    @staticmethod
    def join_room(rooid, uid, nick):
        pass

    @staticmethod
    def leave_room(roomid):
        pass

    @staticmethod
    def invite_members(roomid, members):
        pass

    @staticmethod
    def block(roomid, uid):
        pass

    @staticmethod
    def unblock(roomid, uid):
        pass

    
class Buddy(models.Model):
    pass

class History(models.Model):
    pass

class Setting(models.Model):
    pass

class Room(models.Model):
    pass

class Member(models.Model):
    pass

class Blocked(models.Model):
    pass


