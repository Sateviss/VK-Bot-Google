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
import requests


def isint(n):
    try:
        i = int(n)
        return True
    except:
        return False


def remove_escapes(s: str):
    escapes = ['\a', '\b', '\f', '\r', '\v', '\0']
    o = []
    for c in s:
        if c in escapes:
            o.append(" ")
        else:
            o.append(c)
    return "".join(o)


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
        pattern = re.compile(re.escape(m['body']+"<br>© Führer ")+"\(\d+\)\n")
        filt = [i for i in filter(pattern.match, self.quote_lines)]
        if not len(filt) and m['uid'] == 183179115 and m['body'] != "":
            self.add_quote(m['body'] + "<br>© Führer ({0})\n".format(len(self.quote_lines)))
            s += 1
        else:
            f += 1
        return s, f

    def handle_message(self, mess):
        ID = str(mess['chat_id'] if mess.keys().__contains__('chat_id') else mess['uid'])
        if mess['uid'] == 136776175 and mess['body'] == "!stop":
            self.bot.send_message(ID, "--ок, ухажу--")
            subprocess.run("pkill python3", shell=1)
        elif mess['body'] == "!update" and mess['uid'] == 136776175:
            self.bot.send_message(ID, "-принято, обновляюсь-")
            subprocess.run("pkill python3; git pull; nohup python3 main.py -update -{ID} &", shell=1)
        elif mess['body'] == "!help":
            self.bot.send_message(ID, "Список команд:\n"
                                      "!flipcoin - монетка\n"
                                      "!ping - понг\n"
                                      "!pong - пинг\n"
                                      "!help - вывести этот список\n"
                                      "!quote - вывести/добавить цитату многоуважаемого фюрера (!help quote)\n"
                                      "!stop - выключить бота (только для автора бота)\n"
                                      "!update - обновить до последней версии (только для автора бота)\n"
                                      "!v - вычислить значение выражения (!help v)\n"
                                      "!yt - скачать видео с YouTube и загрузить его в вк, по ID")
        elif mess['body'] == "!help v":
            self.bot.send_message(ID, "Список команд, разрешенных в !v:\n" + str("".join([i+"\n" for i in self.safe_dict.keys()])))
        elif mess['body'] == "!help quote":
            self.bot.send_message(ID, "Подкоманды !quote:\n"
                                      "!quote - вывести случайную цитату\n"
                                      "!quote N - вывести цитату номер N (N - целое число)\n"
                                      "!quote и переслать сообщение Фюрера - добавить цитату в пул\n"
                                      "!quote all - скачать все цитаты, которые были ранее пересланы\n"
                                      "!quote get - получить файл со списком цитат\n"
                                      "!quote last - вывести последнюю добавленную цитату\n")
        elif "[id" + str(self.me) + "|" in mess['body']:
            user = self.bot.get_user(mess['uid'])
            self.bot.send_message(ID, "[id" + str(mess['uid']) + "|" + user['first_name'] + " " + user['last_name'] + "], отъебись блять")
        elif mess['body'] == "!ping":
            self.bot.send_message(ID, "понг")
        elif mess['body'] == "!pong":
            self.bot.send_message(ID, "пинг")
        elif mess['body'] == "!flipcoin":
            self.bot.send_message(ID, random.choice(['орёл', 'решка']))
        elif mess['body'][:2] == "!v":
            try:
                a = re.sub("print\s*\((.+)\)", "\"$1\"", mess['body'].replace("!v", ''))
                print(a)
                o = remove_escapes(str(simple_eval(a, functions=self.safe_dict)))
                if len(o.split()) == 0 or len(o) == 0:
                    self.bot.send_message(ID, "[id" + str(mess['uid']) + "|ПИДОР]!")
                else:
                    self.bot.send_message(ID, o)
            except:
                self.bot.send_message(ID, "-error-")
        elif mess['body'][:3] == "!yt":
            link = mess['body'].replace("!yt ", '')
            print(link)
            self.bot.send_message(ID, youtube.down_and_send(link, ID, self.bot))
        elif mess['body'][:6] == "!quote" and mess['uid'] != 183179115:
            if mess['body'] == "!quote":
                if "fwd_messages" in mess.keys():
                    s, f = self.mess_bfs(mess, 0, 0)
                    self.bot.send_message(ID, "--добавлено {0} сообщений, не добавлено {1} сообщений--".format(s, f-1))
                else:
                    if len(self.quote_lines):
                        self.bot.send_message(ID, random.choice(self.quote_lines))
                    else:
                        self.bot.send_message(ID, "--Цитат пока что нет--")
            if len(mess['body'].split()) > 1:
                if mess['body'] == "!quote all":
                    le = 100
                    total = 0
                    s = 0
                    while le == 100:
                        arr = self.bot.msg_search("!quote", 100, total)
                        for m in arr:
                            total += 1
                            if "fwd_messages" in m.keys() and m['uid'] != 183179115 and m['body'] == "!quote":
                                s1, f1 = self.mess_bfs(m, 0, 0)
                                s += s1
                        le = len(arr)
                    self.bot.send_message(ID, "--Добавлено {0} сообщений--".format(s))
                elif isint(mess['body'].split()[1]):
                    n = int(mess['body'].split()[1])
                    if abs(n) < len(self.quote_lines):
                        self.bot.send_message(ID, self.quote_lines[n])
                    else:
                        self.bot.send_message(ID, "--Столько цитат ещё не добавлено, пока что их {0}--".format(len(self.quote_lines)))
                elif mess['body'] == "!quote last":
                    self.bot.send_message(ID, self.quote_lines[-1])
                elif mess['body'] == "!quote get":
                    url = self.bot.doc_get_url()
                    f = open("quotes.txt", 'rb')
                    r = requests.post(url=url, files={'file': f}).json()
                    file = self.bot.doc_save(r['file'])[0]
                    string = "doc{0}_{1}".format(str(file['owner_id']), str(file['did']))
                    self.bot.send_attachment(ID, "лови", string)
        if mess['uid'] == 445077792:
            self.nahui.append([self.bot.send_message(ID, "[id445077792|Юра], иди нахуй"), time.time() + 20])
            print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Юра нахуй")
        if (mess['uid'] == 461460001 or mess['uid'] == 463718240) and 'attachments' in mess.keys():
            self.bot.send_message(ID, self.bot.gen_sage(49))
            self.bot.send_message(ID, "АНТИПОРН")
            print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Антипорн!")