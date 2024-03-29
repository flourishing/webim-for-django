#!/usr/bin/env python
#coding: utf-8

class Plugin(object):

    @staticmethod
    def buddies(uid):
        #TODO
        buddy = lambda i: { 
                'id': "%d" % (i), 
                'nick': 'user%d' % (i), 
                'presence': 'offline', 
                'show': 'unavailable', 
                'avatar': 'static/webim/images/male.png'
                }
        return [ buddy(i) for i in range(1, 11) ]

    @staticmethod
    def buddies_by_ids(uid, ids):
        return []

    @staticmethod
    def members(roomid):
        return []
    @staticmethod
    def rooms(uid):
        return []

    @staticmethod
    def notifications(uid):
        #TODO
        return [{'text': 'Notification', 'link': '#'}]

    @staticmethod
    def menu(uid):
        return []

    @staticmethod
    def find_room(roomid):
        return None


