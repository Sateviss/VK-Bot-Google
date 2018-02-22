#!/usr/bin/python3
# -*- coding: utf-8 -*-

from wrap import VkWrap
from simpleeval import simple_eval
import math
import time
import os
import re
import youtube
import subprocess


class Handler:
    me = -1
    t = -1
    nahui = []
    def __init__(self, wrapper: VkWrap, safe_list):
        self.bot = wrapper
        self.safe_dict = {k.__name__: k for k in safe_list}
        self.nahui = []
        self.me = self.bot.get_user()['uid']
        self.t = time.time()+60
        self.last_message = -1

    def handle_message(self, mess):
        ID = str(mess['chat_id'] if mess.keys().__contains__('chat_id') else mess['uid'])
        if mess['uid'] == 136776175 and mess['body'] == "!stop":
            self.bot.send_message(ID, "--ок, ухажу--")
            subprocess.run("pkill python3", shell=1)
        elif mess['body'] == "!help":
            self.bot.send_message(ID, "Список комманд:\n"
                                      "\t!help - вывести этот список\n"
                                      "\t!ping - понг\n"
                                      "\t!pong - пинг\n"
                                      "\t!stop - выключить бота (только для автора бота)\n"
                                      "\t!v - вычислить значение выражения (!help v чтобы вывести список команд)\n"
                                      "\t!yt - скачать видео с YouTube и загрузить его в вк, по ID\n")
        elif mess['body'] == "!help v":
            self.bot.send_message(ID, "Список команд, разрешенных в !v:\n" + str("".join([i+" " for i in self.safe_dict.keys()])))
        elif "[id" + str(self.me) + "|" in mess['body']:
            user = self.bot.get_user(mess['uid'])
            self.bot.send_message(ID, "[id" + str(mess['uid']) + "|" + user['first_name'] + " " + user['last_name'] + "], отъебись блять")
        elif mess['body'] == "!ping":
            self.bot.send_message(ID, "понг")
        elif mess['body'] == "!pong":
            self.bot.send_message(ID, "пинг")
        elif mess['body'][:2] == "!v":
            try:
                a = re.sub("print\s*\((.+)\)", "\"$1\"", mess['body'].replace("!v", ''))
                print(a)
                o = str(simple_eval(a, functions=self.safe_dict))
                if len(o.split()) == 0:
                    self.bot.send_message(ID, "[id" + str(mess['uid']) + "|ПИДОР]!")
                else:
                    self.bot.send_message(ID, o)
            except:
                self.bot.send_message(ID, "-error-")
        elif mess['body'][:3] == "!yt":
            link = mess['body'].replace("!yt ", '')
            print(link)
            self.bot.send_message(ID, youtube.down_and_send(link, ID, self.bot))
        if mess['uid'] != self.me:
            self.last_message = mess['mid']
            if mess['uid'] == 445077792:
                self.nahui.append([self.bot.send_message(ID, "[id445077792|Юра], иди нахуй"), time.time() + 20])
                print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Юра нахуй")
            if (mess['uid'] == 461460001 or mess['uid'] == 463718240) and 'attachments' in mess.keys():
                self.bot.send_message(ID, self.bot.gen_sage(49))
                self.bot.send_message(ID, "АНТИПОРН")
                print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Антипорн!")