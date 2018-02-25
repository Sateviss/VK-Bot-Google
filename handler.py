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
import io
import random


class Handler:
    me = -1
    t = -1
    nahui = []

    def __init__(self, wrapper: VkWrap, safe_list):
        self.bot = wrapper
        self.safe_dict = {k.__name__: k for k in safe_list}
        self.nahui = []
        self.me = self.bot.me
        self.t = time.time()+60
        self.last_message = -1
        self.quote_lines = io.open("quotes.txt", mode="r", encoding="UTF-8").readlines()

    def add_quote(self, quote):
        self.quote_lines.append(quote)
        with io.open("quotes.txt", mode="a", encoding="UTF-8") as f:
            f.write(quote)

    def mess_bfs(self, m, s, f):
        if "fwd_messages" in m.keys():
            for fwd in m['fwd_messages']:
                s, f = self.mess_bfs(fwd, s, f)
        if (m['body'] + " © Führer\n") not in self.quote_lines and m['uid'] == 183179115 and m['body'] != "":
            self.add_quote(m['body'] + " © Führer\n")
            s += 1
        else:
            f += 1
        return s, f

    def handle_message(self, mess):
        ID = str(mess['chat_id'] if mess.keys().__contains__('chat_id') else mess['uid'])
        if mess['uid'] == 136776175 and mess['body'] == "!stop":  #стоп бота
            self.bot.send_message(ID, "--ок, ухажу--")
            subprocess.run("pkill python3", shell=1)
        elif mess['body'] == "!help":   #help 
            self.bot.send_message(ID, "Список команд:\n"
                                      "\t!help - вывести этот список\n"
                                      "\t!ping - понг\n"
                                      "\t!pong - пинг\n"
                                      "\t!stop - выключить бота (только для автора бота)\n"
                                      "\t!v - вычислить значение выражения (!help v чтобы вывести список команд)\n"
                                      "\t!yt - скачать видео с YouTube и загрузить его в вк, по ID\n"
                                      "\t!quote - вывести/добавить цитату многоуважаемого фюрера\n")
        elif mess['body'] == "!help v":  #help по выражениям
            self.bot.send_message(ID, "Список команд, разрешенных в !v:\n" + str("".join([i+" " for i in self.safe_dict.keys()])))
        elif mess['body'] == "!help quote": #help по цитатнику фюрера
            self.bot.send_message(ID, "Напишите !quote чтобы получить случайную цитату фюрера, или перешлите его "
                                      "сообщение, с командой !quote чтобы добавить его в пул")
        elif "[id" + str(self.me) + "|" in mess['body']:
            user = self.bot.get_user(mess['uid'])
            self.bot.send_message(ID, "[id" + str(mess['uid']) + "|" + user['first_name'] + " " + user['last_name'] + "], отъебись блять")
        elif mess['body'] == "!ping":  #пинг понг
            self.bot.send_message(ID, "понг")
        elif mess['body'] == "!pong":   #понг пинг
            self.bot.send_message(ID, "пинг")
        elif mess['body'] == "!flipcoin":  # собственно , монетка
            self.bot.send_message(ID, random.choice(['орёл', 'решка'])) 
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
        elif mess['body'][:3] == "!yt":    #Подгрузка видео с ютуба
            link = mess['body'].replace("!yt ", '')
            print(link)
            self.bot.send_message(ID, youtube.down_and_send(link, ID, self.bot))
        elif mess['body'] == "!quote" and mess['uid'] != 183179115:
            if "fwd_messages" in mess.keys():
                s, f = self.mess_bfs(mess, 0, 0)
                self.bot.send_message(ID, "--добавлено {0} сообщений, не добавлено {1} сообщений--".format(s, f-1))
            else:
                if len(self.quote_lines):
                    self.bot.send_message(ID, random.choice(self.quote_lines))
                else:
                    self.bot.send_message(ID, "--Цитат пока что нет--")
        elif mess['body'] == "!quote all" and mess['uid'] == 136776175:
            le = 100
            total = 0
            s = 0
            f = 0
            while le == 100:
                arr = self.bot.msg_search("!quote", 100, total)
                for m in arr:
                    total += 1
                    if "fwd_messages" in m.keys() and m['uid'] != 183179115 and m['body'] == "!quote":
                        s1, f1 = self.mess_bfs(m, 0, 0)
                        s += s1
                        f += f1
                le = len(arr)
                self.bot.send_message(ID, "--добавлено {0} сообщений, не добавлено {1} сообщений--".format(s, f - total))
        if mess['uid'] == 445077792: #Шлём Юру нах
            self.nahui.append([self.bot.send_message(ID, "[id445077792|Юра], иди нахуй"), time.time() + 20])
            print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Юра нахуй")
        if mess['uid'] == 182192214: #Паша пришел
            self.nahui.append([self.bot.send_message(ID, "[id182192214|Сентябрь] горит"), time.time() + 40])
            print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Сентябрь приплелся")

        if (mess['uid'] == 461460001 or mess['uid'] == 463718240) and 'attachments' in mess.keys(): #Шлём нах ботов с проном
            self.bot.send_message(ID, self.bot.gen_sage(49))
            self.bot.send_message(ID, "АНТИПОРН")
            print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Антипорн!")
