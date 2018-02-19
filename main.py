# -*- coding: utf-8 -*-

import re
import time
import sys
import wrap
import math
import threading
import youtube

file = open("login.txt", "r")
login = file.readline().replace('\n', '')
password = file.readline().replace('\n', '')
file.close()

wrap.log_in(login, password)

print("...working")
#wrap.send_message(ID, "---Бот Запущен---")
last_messages = {}
last_message = -1
nahui = []
me = wrap.get_user()['uid']

safe_list = [math.acos, math.asin, math.atan, math.atan2, math.ceil, math.cos, math.cosh, math.degrees,
             math.exp, math.fabs, math.floor, math.fmod, math.frexp, math.hypot, math.ldexp, math.log, math.log10,
             math.modf, math.pow, math.radians, math.sin, math.sinh, math.sqrt, math.tan, math.tanh]

safe_dict = {k.__name__: k for k in safe_list}

t = time.time()+60

while 1:
    mess = wrap.get_inbox()
    i = 0
    while i < len(nahui):
        if nahui[i][1] < time.time():
            wrap.delete_message(nahui[i][0])
            nahui.pop(i)
            continue
        i += 1
    if time.time() > t:
        wrap.cleanup_videos(24*3600)
        t = time.time()+60
    if last_message != mess['mid']:
        ID = str(mess['chat_id'] if mess.keys().__contains__('chat_id') else mess['uid'])
        if not last_messages.keys().__contains__(ID):
            last_messages.update({ID: mess['mid']})
        else:
            last_message = last_messages[ID]
        if mess['body'] == "!help":
            wrap.send_message(ID, "Список комманд:\n"
                                  "\t!help - вывести этот список\n"
                                  "\t!ping - понг\n"
                                  "\t!stop - выключить бота (только для автора бота)\n"
                                  "\t!v - вычислить значение выражения (!help v чтобы вывести список команд)\n"
                                  "\t!yt - скачать видео с YouTube и загрузить его в вк, по ID\n")
        if mess['body'] == "!help v":
            safe_dict = [k.__name__ for k in safe_list]
            wrap.send_message(ID, "Список команд, разрешенных в !v:\n"+str(safe_dict))
        if mess['uid'] == 136776175 and mess['body'] == "!stop":
            wrap.send_message(ID, "--ок, ухажу--")
            sys.exit(0)
        if mess['body'] == "!ping":
            wrap.send_message(ID, "понг")
        if mess['body'][:2] == "!v":
            try:
                safe_dict = {k.__name__: k for k in safe_list}
                a = re.sub("print\s*\((.+)\)", "\"$1\"", mess['body'].replace("!v", ''))
                print(a)
                wrap.send_message(ID, str(eval(a, {'e': math.e, 'pi': math.pi}, safe_dict)))
            except:
                wrap.send_message(ID, "-error-")
        if mess['body'][:3] == "!yt":
            link = mess['body'].replace("!yt ", '')
            print(link)
            threading._start_new_thread(wrap.send_message, (ID, youtube.down_and_send(link, ID)))
        if mess['uid'] != me:
            user = wrap.get_user(mess['uid'])
            last_message = mess['mid']
            if mess['uid'] == 445077792:
                nahui.append([wrap.send_message(ID, "Юра, иди нахуй"), time.time() + 10])
                print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Юра нахуй")
            if (mess['uid'] == 461460001 or mess['uid'] == 463718240) and 'attachments' in mess.keys():
                wrap.send_message(ID, wrap.gen_message(49))
                wrap.send_message(ID, "АНТИПОРН")
                print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Антипорн!")

