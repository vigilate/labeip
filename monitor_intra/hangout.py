#!/usr/bin/env python3
## hangout.py for  in /home/eax/dev/vigilate/labeip/monitor_intra
## 
## Made by eax
## Login   <soules_k@epitech.net>
## 
## Started on  Tue Mar  3 01:11:05 2015 eax
## Last update Tue Mar  3 02:35:34 2015 eax
##

import signal
import asyncio
import hangups

class MyHangBot():

    def __init__(self):
        self.client = None
        self.user = None
        self.convs = None
        self.connectMsg = None
        self.bot_username = open("hangout_name").read().strip()

    
    def get_creds(self):
        mail = None
        pwd = None
        with open("hangout_creds") as f:
            mail, pwd = f.read().strip().split(" ", 1)
        return mail, pwd

    def set_connect_msg(self, convid, msg):
        self.connectMsg = {"id": convid, "msg": msg}
    
    def login(self):
        cookie = None
        try:
            cookies = hangups.auth.get_auth(self.get_creds, False, ".cookies.json")
        except hangups.GoogleAuthError as e:
            print("fail connect: %s" % e)
            return False

        self.client = hangups.Client(cookies)
        self.client.on_connect.add_observer(self.on_connect)
        
        return True

    def on_connect(self, data):
        print("on_connect")
        self.users = hangups.UserList(self.client, data.self_entity, data.entities, data.conversation_participants)
        
        self.convs = hangups.ConversationList(self.client, data.conversation_states, self.users, data.sync_timestamp)
        
        self.user_id = self.get_user_id()


        if self.connectMsg:
            self.send_msg(self.connectMsg["id"], self.connectMsg["msg"])
        
    def stop(self, _=False):
        print ("forced stop")
        asyncio.async(self.client.disconnect()).add_done_callback(lambda future: future.result())
        exit("stoped")


    def get_user_id(self):
        for c in self.convs.get_all():
            for u in c.users:
                if u.full_name == self.bot_username:
                    return u.id_
        return None

    def get_conv_by_id(self, id_):
        for c in self.convs.get_all():
            if c.id_ == id_:
                return c
        return None
        
    def send_msg(self, conv_id, msg, killme=True):
        conv = self.get_conv_by_id(conv_id)
        asyncio.async(conv.send_message([hangups.ChatMessageSegment(msg)])).add_done_callback(self.stop)
