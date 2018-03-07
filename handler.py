#!/usr/bin/python3
# -*- coding: utf-8 -*-

import io
import os
import platform
import queue
import random
import re
import subprocess
import time
import logging

import praw
import pyshorteners
import requests
from simpleeval import simple_eval

import youtube
from wrap import VkWrap
import json

reddit_img_url_len = len("https://i.redd.it/oqnxnvhpts201.jpg") + 2

message_regex = re.compile(r'^[\\/!]\w+')


def isint(n: str):
    if not n.isdigit():
        return n.replace('-', '', 1).isdigit()
    return True


def remove_escapes(message: str):
    """ Replace all escape characters with spaces """
    escapes = ['\a', '\b', '\f', '\r', '\v', '\0']
    output = []

    for char in message:
        output.append(char if char not in escapes else ' ')

    return ''.join(output)


def gen_factorization(number: int):
    """ Number factorization from 2 to N """
    output = ''

    for i in range(2, number + 1):
        output += str(i) + ": "
        factors = []
        divisor = 2

        while i > 1:
            if i % divisor == 0:
                i /= divisor
                factors.append(divisor)
                divisor = 1
            divisor += 1

        output += str(factors) + '\n'

    return output


class Handler:

    def __init__(self, wrapper: VkWrap, safe_list, google_api_key):

        self.bot = wrapper
        self.safe_dict = {k.__name__: k for k in safe_list}
        self.delete_queue = queue.Queue()
        self.me = self.bot.me
        self.t = time.time() + 60
        self.last_message = -1
        if not os.path.exists("Data/quotes.txt"):
            open("Data/quotes.txt", "wb").close()
        self.quote_lines = io.open("Data/quotes.txt", mode="r", encoding="UTF-8").readlines()
        self.reddit = praw.Reddit(client_id='wG7Qwo-mAbkSoQ',
                                  client_secret='FUrav__HGF0e08Vv6CJBfk-bCrA',
                                  user_agent='Marvin')

        self.admins = ['136776175', '118781407']  # Eugene and Dmitry
        if not os.path.exists("Data/greetings.json"):
            self.greetings = {}
            open("Data/greetings.json", "w").close()
        else:
            self.greetings = json.load(open("Data/greetings.json"))
        func_list = [self.r, self.changelog, self.stop, self.update,
                     self.help, self.ping, self.pong, self.flipcoin,
                     self.v, self.yt, self.quote, self.stats]
        self.func_dict = {k.__name__: k for k in func_list}
        self.func_usage = {k.__name__: 0 for k in func_list}
        self.greet_usage = {k: 0 for k in self.greetings.keys()}
        self.shortener = pyshorteners.Shortener('Google', api_key=google_api_key)
        self.start_time = time.time()

    def greeting(self, mess, ID):
        message = self.bot.send_message(ID, self.greetings[mess['user_id']]['greeting'])
        self.delete_queue.put((message, time.time() + self.greetings[mess['user_id']]['timeout']))

    def r(self, mess, ID):
        mess['body'] = mess['body'].replace("/", " ")
        subreddit = mess['body'].split()[1]
        com = mess['body'].split()[0] + ("" if len(mess['body'].split()) == 2 else " " + mess['body'].split()[2])
        if com == "r" or com == "r hot":
            subs = [k for k in self.reddit.subreddit(subreddit).hot()]
        elif com == "r new":
            subs = [k for k in self.reddit.subreddit(subreddit).new()]
        elif com == "r rising":
            subs = [k for k in self.reddit.subreddit(subreddit).rising()]
        elif com == "r top":
            subs = [k for k in self.reddit.subreddit(subreddit).top()]
        else:
            raise Exception("Improper format Provided: " + com)
        nums = [i for i in range(len(subs))]
        while len(nums):
            i = random.choice(nums)
            s = subs[i]
            nums.remove(i)
            try:
                im_url = s.preview['images'][0]['source']['url']
                print(im_url)
            except Exception:
                continue
            if ".jpg" in im_url:
                if s.over_18:  # and ID != mess['user_id']:
                    self.bot.send_message(ID, "NSFW: {0}, но для желающих ссылка: {1}".format(
                        subreddit, (self.shortener.short(im_url) if len(im_url) > reddit_img_url_len else im_url)))
                else:
                    f = requests.get(im_url).content
                    url = self.bot.get_photo_link()['upload_url']
                    file = open(str(hash(f)) + ".jpg", "wb")
                    file.write(f)
                    file.close()
                    r = requests.post(url=url, files={'photo': open(str(hash(f)) + ".jpg", "rb")}).json()
                    p = self.bot.save_photo(**r)
                    os.remove(str(hash(f)) + ".jpg")
                    self.bot.send_attachment(ID, "", "photo{0}_{1}".format(p['owner_id'], p['id']))
                return
        raise Exception("No Pics")

    def changelog(self, mess, ID):
        c = io.open("changelog", mode="r", encoding="UTF-8")
        self.bot.send_message(ID, c.read())

    def stop(self, mess, ID):
        if mess['user_id'] in self.admins:
            self.bot.send_message(ID, "ок, ухажу")
            if platform.system() == "Windows":
                subprocess.run("taskkill /f /im python.exe", shell=True)
            subprocess.run("pkill python3", shell=True)

    def update(self, mess, ID):
        if mess['user_id'] in self.admins:
            self.bot.send_message(ID, "принято, обновляюсь")
            if "Windows" == platform.system():
                subprocess.run(
                    args="taskkill /f /im python.exe && git pull && start python.exe main.py update {0}".format(ID),
                    shell=True
                )
            subprocess.run("pkill python3; git pull; nohup python3 main.py update {0} &".format(ID), shell=True)

    def help(self, mess, ID):
        if mess['body'] == "help":
            c = io.open("help/help", mode="r", encoding="UTF-8")
            self.bot.send_message(ID, c.read())
            return
        else:
            try:
                c = io.open("help/" + mess['body'].split()[1], mode="r", encoding="UTF-8")
                self.bot.send_message(ID, c.read())
                return
            except:
                self.bot.send_message(ID, "Такого файла помощи не существует")

    def ping(self, mess, ID):
        self.bot.send_message(ID, "понг ({0} мс)".format(int(1000 * (time.time() - mess['date']))))

    def pong(self, mess, ID):
        self.bot.send_message(ID, "пинг")

    def flipcoin(self, mess, ID):
        self.bot.send_message(ID, random.choice(['орёл', 'решка']))

    def v(self, mess, ID):
        try:
            a = re.sub("print\s*\((.+)\)", "\"$1\"", mess['body'][1:])
            a.replace("&quot;", "\"")
            print(a)
            o = remove_escapes(str(simple_eval(a, functions=self.safe_dict)))
            if len(o.split()) == 0 or len(o) == 0:
                self.bot.send_message(ID, "[id" + mess['user_id'] + "|ПИДОР]!")
            else:
                self.bot.send_message(ID, o + " [id{0}|©]".format(mess['user_id']))
        except Exception as e:
            raise e

    def yt(self, mess, ID):
        link = mess['body'][-len("7-LPcVo7gC0"):]
        print(link)
        self.bot.send_message(ID, youtube.down_and_send(link, ID, self.bot))

    def quote(self, mess, ID):

        def mess_bfs(message, success, fails):

            def add_quote(quote):
                self.quote_lines.append(quote)
                with io.open("Data/quotes.txt", mode="a", encoding="UTF-8") as quotes_file:
                    quotes_file.write(quote)

            if "fwd_messages" in message.keys():
                for fwd in message['fwd_messages']:
                    success, fails = mess_bfs(fwd, success, fails)
            message['body'] = message['body'].replace('\n', "<br>")
            pattern = re.compile(re.escape(message['body'] + "<br>© Führer ") + "\(\d+\)\n")
            filt = [i for i in filter(pattern.match, self.quote_lines)]
            if not len(filt) and message['user_id'] == '183179115' and message['body'] != "":
                add_quote(message['body'] + "<br>© Führer ({0})\n".format(len(self.quote_lines)))
                success += 1
            else:
                fails += 1
            return success, fails

        if mess['user_id'] == '183179115':
            return
        if mess['body'] == "quote":
            if "fwd_messages" in mess.keys():
                total_successes, f = mess_bfs(mess, 0, 0)
                self.bot.send_message(
                    ID,
                    "Добавлено {0} сообщений, не добавлено {1} сообщений".format(total_successes, f - 1))
            else:
                if len(self.quote_lines):
                    self.bot.send_message(ID, random.choice(self.quote_lines))
                else:
                    self.bot.send_message(ID, "Цитат пока что нет")
        if len(mess['body'].split()) > 1:  # Циатник
            if mess['body'] == "quote all" and mess['user_id'] in self.admins:
                le = 100
                total = 0
                total_successes = 0
                while le == 100:
                    arr = self.bot.msg_search("quote", 100, total)
                    for m in arr:
                        total += 1
                        if "fwd_messages" in m.keys() and m['user_id'] != '183179115' and m['body'][1:] == "quote":
                            total_successes += mess_bfs(m, 0, 0)[0]
                    le = len(arr)
                self.bot.send_message(ID, "Добавлено {0} сообщений".format(total_successes))
            elif isint(mess['body'].split()[1]):
                n = int(mess['body'].split()[1])
                if abs(n) < len(self.quote_lines):
                    self.bot.send_message(ID, self.quote_lines[n])
                else:
                    self.bot.send_message(ID, "Столько цитат ещё не добавлено, пока что их {0}".format(
                        len(self.quote_lines)))
            elif mess['body'] == "quote last":
                self.bot.send_message(ID, self.quote_lines[-1])
            elif mess['body'] == "quote get":
                url = self.bot.doc_get_url()
                r = requests.post(url=url, files={'file': open("Data/quotes.txt", 'rb')}).json()
                file = self.bot.doc_save(r['file'])[0]
                string = "doc{0}_{1}".format(str(file['owner_id']), str(file['id']))
                self.bot.send_attachment(ID, "лови", string)

    def stats(self, mess, ID):
        o = ""
        o += "\nВремя работы: " + time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start_time)) + "\n"
        o += "\nПользователи с правами администратора:\n"
        for a in self.admins:
            o += "• [id{0}|{1} {2}]\n".format(
                a,
                self.bot.get_user(a)['first_name'],
                self.bot.get_user(a)['last_name']
            )
        o += "\nОбработанные запросы:\n"
        total = 0
        for f in self.func_usage.keys():
            if self.func_usage[f]:
                o += "• {0}: {1}\n".format(f, self.func_usage[f])
                total += self.func_usage[f]
        o += "Всего: " + str(total) + "\n"

        o += "\nПриветствия:\n"
        total = 0
        for f in self.greet_usage.keys():
            if self.greet_usage[f]:
                o += "• [id{0}|{1} {2}]: {3}\n".format(f,
                    self.bot.get_user(f)['first_name'],
                    self.bot.get_user(f)['last_name'],
                    self.greet_usage[f]
                )
                total += self.greet_usage[f]
        o += "Всего: " + str(total) + "\n"

        self.bot.send_message(ID, o)

    def greet(self, mess, ID):
        if mess['body'].split()[1] == "me":
            if mess['user_id'] in self.greetings.keys():
                if self.greetings[mess['user_id']]['admined'] and mess['user_id'] not in self.admins:
                    raise Exception("You already have a greeting created by an admin")
            self.greetings.update({ mess['user_id']: {'greeting': mess['body'][len("greet me "):],
                                                      'timeout': 10,
                                                      'admined': mess['user_id'] in self.admins}})
            json.dump(self.greetings, open("Data/greetings.json", "w"), indent=True, ensure_ascii=False)
            self.bot.send_message(ID, 'Добавлено приветствие "{0}"'.format(self.greetings[mess['user_id']]['greeting']))
            self.greet_usage.update({mess['user_id']: 0})
            return
        if mess['body'].split()[1] == 'delete':
            if len(mess['body'].split()) == 2:
                if self.greetings[mess['user_id']]['admined'] and mess['user_id'] not in self.admins:
                    raise Exception("You already have a greeting created by an admin")
                self.greetings.pop(mess['user_id'])
                self.bot.send_message(ID, "Приветствие удалено")
            if len(mess['body'].split()) == 3 and mess['user_id'] in self.admins:
                self.greetings.pop(mess['body'].split()[2])
                self.bot.send_message(ID, "Приветствие удалено")
            return
        if isint(mess['body'].split()[1]) and mess['user_id'] in self.admins:
            self.greetings.update({mess['body'].split()[1]: {'greeting': mess['body'][len("greet "+mess['body'].split()[1])+1:],
                                                     'timeout': 10,
                                                     'admined': mess['user_id'] in self.admins}})
            json.dump(self.greetings, open("Data/greetings.json", "w"), indent=True, ensure_ascii=False)
            self.bot.send_message(ID, 'Добавлено приветствие "{0}"'.format(self.greetings[mess['body'].split()[1]]['greeting']))
            self.greet_usage.update({mess['body'].split()[1]: 0})
            return

    def handle_message(self, mess):
        if 'chat_id' in mess.keys():
            ID = mess['chat_id']
            logging.info("{0} ({1}) {2} {3}: {4}".format(
                time.strftime("%d.%m.%Y %H:%M:%S"),
                self.bot.get_chat(mess['chat_id'])['title'],
                self.bot.get_user(mess['user_id'])['first_name'],
                self.bot.get_user(mess['user_id'])['last_name'],
                mess['body'])
            )
        else:
            ID = mess['user_id']
            logging.info("{0} ({1}) {2} {3}: {4}".format(
                time.strftime("%d.%m.%Y %H:%M:%S"),
                ID,
                self.bot.get_user(mess['user_id'])['first_name'],
                self.bot.get_user(mess['user_id'])['last_name'],
                mess['body'])
            )
        if mess['user_id'] in self.greetings.keys():
            self.greeting(mess, ID)
            self.greet_usage[mess['user_id']] += 1
        if message_regex.match(mess['body']):
            tmp = ('$'+mess['body'][1:]).replace("/", " ")
            com = tmp.split()[0][1:]
            mess['body'] = mess['body'][1:]
        else:
            return

        if "[id{0}|".format(self.bot.me) in mess['body']:
            user = self.bot.get_user(mess['user_id'])
            self.bot.send_message(ID, "[id{0}|{1} {2}], отъебись блять".format(
                mess['user_id'],
                user['first_name'],
                user['last_name'])
            )
        if com in self.func_dict:
            try:
                self.func_usage[com] += 1
                f = self.func_dict[com]
                f(mess, ID)
            except Exception as e:
                self.bot.send_message(ID, "error: {0}".format(e.args))
                raise e
