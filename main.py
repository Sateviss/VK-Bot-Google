# -*- coding: utf-8 -*-
import re

import time
import sys
import wrap
from math import *

file = open("login.txt", "r")
login = file.readline().replace('\n', '')
password = file.readline().replace('\n', '')
file.close()

wrap.log_in(login, password)

ID = 2


print("...working")
wrap.send_message(ID, "---Бот Запущен---")
last_message = -1
nahui = []
me = wrap.get_user()['uid']

safe_list = [acos, asin, atan, atan2, ceil, cos, cosh, degrees,
             exp, fabs, floor, fmod, frexp, hypot, ldexp, log, log10,
             modf, pow, radians, sin, sinh, sqrt, tan, tanh]
safe_dict = {k.__name__: k for k in safe_list}

while 1:
    time.sleep(0.2)
    mess = wrap.get_history(ID)

    i = 0
    while i < len(nahui):
        n = nahui[i]
        if n[1] < time.time():
            wrap.delete_message(n[0])
            nahui.pop(i)
            continue
        n[1] -= 0.2
        i += 1

    if last_message != mess['mid']:
        if mess['body'] == "!help":
            wrap.send_message(ID, "Список комманд:\n"
                                  "\t!help - вывести этот список\n"
                                  "\t!стоп - выключить бота (только для автора бота)\n"
                                  "\t!v - вычислить значение выражения (!help v чтобы вывести список команд)\n")
        if mess['body'] == "!help v":
            safe_dict = [k.__name__ for k in safe_list]
            wrap.send_message(ID, "Список команд, разрешенных в !v:\n"+str(safe_dict))
        if mess['uid'] == 136776175 and mess['body'] == "!стоп":
            wrap.send_message(ID, "--ок, ухажу--")
            sys.exit(0)
        if mess['body'] == "!пинг":
            wrap.send_message(ID, "понг")
        if mess['body'][:2] == "!v":
            try:
                safe_dict = {k.__name__: k for k in safe_list}
                a = re.sub("print\s*\((.+)\)", "\"$1\"", mess['body'].replace("!v ", ''))
                print(a)
                wrap.send_message(ID, "= "+str(eval(a, {'e': e, 'pi': pi}, safe_dict)))
            except:
                wrap.send_message(ID, "-error-")
        if mess['uid'] != me:
            user = wrap.get_user(mess['uid'])
            print(time.strftime("%d.%m.%y - %H:%M:%S "), user['first_name'], user['last_name']+" :"+mess['body'])
            last_message = mess['mid']
            if mess['uid'] == 445077792:
                nahui.append([wrap.send_message(ID, "Юра, иди нахуй"), time.time() + 10])
                print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Юра нахуй")
            if (mess['uid'] == 461460001 or mess['uid'] == 463718240 or mess['uid'] == 465167934) and mess['body'] == '':
                wrap.send_message(ID, wrap.gen_message(49))
                wrap.send_message(ID, "АНТИПОРН")
                print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Антипорн!")

