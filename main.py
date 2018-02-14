# -*- coding: utf-8 -*-
import re

import vk
import time
import sys
from math import *
from datetime import datetime

file = open("login.txt", "r")
login = file.readline().replace('\n', '')
password = file.readline().replace('\n', '')
file.close()

session = vk.AuthSession(app_id=6322567, user_login=login, user_password=password, scope=268435455)
api = vk.API(session)
ID = 1

user_dict = {}

def get_message(c_id):
    delay = 0.01
    while 1:
        try:
            mess = api.messages.getHistory(chat_id=c_id, count=1)[1]
            return mess
        except:
            time.sleep(delay)
            delay *= 2
            continue


def send_message(c_id, text):
    delay = 0.01
    while 1:
        try:
            if len(text) < 4000:
                m = api.messages.send(chat_id=c_id, message=text)
            else:
                m = api.messages.send(chat_id=c_id, message="Очень длинное сообщение, которое начинается на "+text[:100])
            return m
        except:
            time.sleep(delay)
            delay *= 2
            continue


def delete_message(m_id):
    delay = 0.01
    while 1:
        try:
            api.messages.delete(message_ids=m_id, delete_for_all=1)
            return
        except:
            time.sleep(delay)
            delay *= 2
            continue


def get_user(u_id=None):
    delay = 0.01
    if user_dict.keys().__contains__(u_id):
        return user_dict[u_id]
    else:
        while 1:
            try:
                if u_id is not None:
                    u = api.users.get(user_id=u_id)[0]
                else:
                    u = api.users.get()[0]
                user_dict.update({u_id:u})
                return u
            except:
                time.sleep(delay)
                delay *= 2
                continue


def gen_message(n):
    o = ''
    for i in range(n - 2):
        i += 2
        o += str(i) + ": "
        k = []
        x = 2
        while i != 1:
            if i % x == 0:
                i /= x
                k.append(x)
                x = 1
            x += 1
        o += str(k) + "\n"
    return o


print("...working")
send_message(ID, "---Бот Запущен---")
last_message = -1
nahui = []
me = get_user()['uid']


while 1:
    time.sleep(0.2)
    mess = get_message(ID)

    i = 0
    while i < len(nahui):
        n = nahui[i]
        if n[1] < time.time():
            delete_message(n[0])
            nahui.pop(i)
            continue
        n[1] -= 0.2
        i += 1

    if last_message != mess['mid']:
        user = get_user(mess['uid'])
        print(time.strftime("%d.%m.%y - %H:%M:%S "), user['first_name'], user['last_name']+" :"+mess['body'])
        last_message = mess['mid']
        if mess['body'] == "!help":
            send_message(ID, "Список комманд:\n"
                             "\t!help - вывести этот список\n"
                             "\t!стоп - выключить бота (только для автора бота)\n"
                             "\t!пинг - понг\n"
                             "\t!v - вычислить значение выражения (!help v чтобы вывести список команд)\n")
        if mess['body'] == "!help v":
            safe_list = [acos, asin, atan, atan2, ceil, cos, cosh, degrees,
                         exp, fabs, floor, fmod, frexp, hypot, ldexp, log, log10,
                         modf, pow, radians, sin, sinh, sqrt, tan, tanh]
            safe_dict = [k.__name__ for k in safe_list]
            send_message(ID, "Список команд, разрешенных в /v:\n"+str(safe_dict))
        if mess['uid'] == 136776175 and mess['body'] == "!стоп":
            send_message(ID, "--ок, ухажу--")
            sys.exit(0)
        if mess['body'] == "!пинг":
            send_message(ID, "понг")
        if mess['body'][:2] == "!v":
            try:
                safe_list = [acos, asin, atan, atan2, ceil, cos, cosh, degrees,
                             exp, fabs, floor, fmod, frexp, hypot, ldexp, log, log10,
                             modf, pow, radians, sin, sinh, sqrt, tan, tanh]
                safe_dict = {k.__name__: k for k in safe_list}
                a = re.sub("print\s*\((.+)\)", "\"$1\"", mess['body'].replace("/v ", ''))
                print(a)
                send_message(ID, str(eval(a, {'e': e, 'pi': pi}, safe_dict)))
            except:
                send_message(ID, "-error-")
        if mess['uid'] != me:
            if mess['uid'] == 445077792:
                nahui.append([send_message(ID, "Юра, иди нахуй"), time.time() + 10])
                print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Юра нахуй")
            if (mess['uid'] == 461460001 or mess['uid'] == 463718240 or mess['uid'] == 465167934) and mess['body'] == '':
                send_message(ID, gen_message(49))
                send_message(ID, "АНТИПОРН")
                print(time.strftime("%d.%m.%y - %H:%M:%S ", time.localtime()), "Антипорн!")

