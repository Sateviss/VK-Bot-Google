#!/usr/bin/python3
# -*- coding: utf-8 -*-

import io
import os
import queue
import random
import re
import subprocess
import time
import platform

import praw
import pyshorteners
import requests
from simpleeval import simple_eval

import youtube
from wrap import VkWrap

reddit_img_url_len = len("https://i.redd.it/oqnxnvhpts201.jpg") + 2

message_regex = re.compile(r'^[\\/!]\w+')


def isint(n: str):
    return n.isdigit()


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

    def __init__(self, wrapper: VkWrap, safe_list, logger, googlAPIkey):
        self.bot = wrapper
        self.safe_dict = {k.__name__: k for k in safe_list}
        self.nahui = queue.Queue()
        self.me = self.bot.me
        self.t = time.time()+60
        self.last_message = -1
        if not os.path.exists("quotes.txt"):
            f = open("quutes.txt", "wb")
            f.close()
        self.quote_lines = io.open("quotes.txt", mode="r", encoding="UTF-8").readlines()
        self.reddit = praw.Reddit(client_id='wG7Qwo-mAbkSoQ',
                                  client_secret='FUrav__HGF0e08Vv6CJBfk-bCrA',
                                  user_agent='Marvin')

        self.admins = [136776175, 118781407]  # Eugene and Dmitry
        self.greetings = {165211652: ["Привет, [id165211652|Женя]", 20],
                          445077792: ["[id445077792|Юра], иди нахуй", 20],
                          182192214: ["[id182192214|Сентябрь] горит", 40],
                          463718240: [str(gen_factorization(48)) + "АНТИСРАМ", 10000000000]}
        func_list = [self.r, self.changelog, self.stop, self.update, self.help, self.ping, self.pong, self.flipcoin,
                     self.v, self.yt, self.quote]
        self.func_dict = {k.__name__: k for k in func_list}
        self.logger = logger
        self.shortener = pyshorteners.Shortener('Google', api_key=googlAPIkey)

    def mess_bfs(self, m, s, f):

        def add_quote(quote):
            self.quote_lines.append(quote)
            with io.open("quotes.txt", mode="a", encoding="UTF-8") as f:
                f.write(quote)

        if "fwd_messages" in m.keys():
            for fwd in m['fwd_messages']:
                s, f = self.mess_bfs(fwd, s, f)
        pattern = re.compile(re.escape(m['body']+"<br>© Führer ")+"\(\d+\)\n")
        filt = [i for i in filter(pattern.match, self.quote_lines)]
        if not len(filt) and m['user_id'] == 183179115 and m['body'] != "":
            add_quote(m['body'] + "<br>© Führer ({0})\n".format(len(self.quote_lines)))
            s += 1
        else:
            f += 1
        return s, f

    def r(self, mess, ID):
        subreddit = mess['body'].split()[1]
        com = mess['body'].split()[0]+("" if len(mess['body'].split()) == 2 else " "+mess['body'].split()[2])
        if com == "r" or com == "r hot":
            subs = [k for k in self.reddit.subreddit(subreddit).hot()]
        elif com == "r new":
            subs = [k for k in self.reddit.subreddit(subreddit).new()]
        elif com == "r rising":
            subs = [k for k in self.reddit.subreddit(subreddit).rising()]
        elif com == "r top":
            subs = [k for k in self.reddit.subreddit(subreddit).top()]
        else:
            raise Exception("Improper format Provided: "+com)
        nums = [i for i in range(len(subs))]
        while len(nums):
            i = random.choice(nums)
            s = subs[i]
            nums.remove(i)
            try:
                im_url = s.preview['images'][0]['source']['url']
                print(im_url)
            except Exception as e:
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
                c = io.open("help/"+mess['body'].split()[1], mode="r", encoding="UTF-8")
                self.bot.send_message(ID, c.read())
                return
            except:
                self.bot.send_message(ID, "Такого файла помощи не существует")

    def ping(self, mess, ID):
        self.bot.send_message(ID, "понг ({0} мс)".format(int(1000*(time.time()-mess['date']))))

    def pong(self, mess, ID):
            self.bot.send_message(ID, "пинг")

    def flipcoin(self, mess, ID):
        self.bot.send_message(ID, random.choice(['орёл', 'решка']))

    def v(self, mess, ID):
        try:
            a = re.sub("print\s*\((.+)\)", "\"$1\"", mess['body'].replace("v", ''))
            a.replace("&quot;", "\"")
            print(a)
            o = remove_escapes(str(simple_eval(a, functions=self.safe_dict)))
            if len(o.split()) == 0 or len(o) == 0:
                self.bot.send_message(ID, "[id" + str(mess['user_id']) + "|ПИДОР]!")
            else:
                self.bot.send_message(ID, o + " [id{0}|©]".format(mess['user_id']))
        except:
            self.bot.send_message(ID, "-error-")

    def yt(self, mess, ID):
        link = mess['body'][-len("7-LPcVo7gC0"):]
        print(link)
        self.bot.send_message(ID, youtube.down_and_send(link, ID, self.bot))

    def quote(self, mess, ID):
        mess = self.bot.get_message(mess['id'])
        mess['body'] = mess['body'][1:]
        if mess['user_id'] == 183179115:
            return
        if mess['body'] == "quote":
            if "fwd_messages" in mess.keys():
                s, f = self.mess_bfs(mess, 0, 0)
                self.bot.send_message(ID, "Добавлено {0} сообщений, не добавлено {1} сообщений".format(s, f - 1))
            else:
                if len(self.quote_lines):
                    self.bot.send_message(ID, random.choice(self.quote_lines))
                else:
                    self.bot.send_message(ID, "Цитат пока что нет")
        if len(mess['body'].split()) > 1:  # Циатник
            if mess['body'] == "quote all" and mess['user_id'] == 136776175:
                le = 100
                total = 0
                s = 0
                while le == 100:
                    arr = self.bot.msg_search("quote", 100, total)
                    for m in arr:
                        total += 1
                        if "fwd_messages" in m.keys() and m['user_id'] != 183179115 and m['body'] == "!quote":
                            s1, f1 = self.mess_bfs(m, 0, 0)
                            s += s1
                    le = len(arr)
                self.bot.send_message(ID, "Добавлено {0} сообщений".format(s))
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
                r = requests.post(url=url, files={'file': open("quotes.txt", 'rb')}).json()
                file = self.bot.doc_save(r['file'])[0]
                string = "doc{0}_{1}".format(str(file['owner_id']), str(file['id']))
                self.bot.send_attachment(ID, "лови", string)

    def greet(self, mess, ID):
        m = self.bot.send_message(ID, self.greetings[mess['user_id']][0])
        self.nahui.put([m, time.time()+self.greetings[mess['user_id']][1]])

    def handle_message(self, mess):
        if 'chat_id' in mess.keys():
            ID = mess['chat_id']
            self.logger.info("{0} ({1}) {2}: {3}".format(time.strftime("%d.%m.%Y %H:%M:%S"),
                                                         self.bot.get_chat(mess['chat_id']),
                                                         self.bot.get_user(mess['user_id']),
                                                         mess['body']))
        else:
            ID = mess['user_id']
            self.logger.info("{0} ({1}) {2}: {3}".format(time.strftime("%d.%m.%Y %H:%M:%S"),
                                                         "PM",
                                                         self.bot.get_user(mess['user_id']),
                                                         mess['body']))
        if message_regex.match(mess['body']):
            com = mess['body'].split()[0][1:]
            mess['body'] = mess['body'][1:]
        else:
            return

        if "[id{0}|".format(self.bot.me) in mess['body']:
            user = self.bot.get_user(mess['user_id'])
            self.bot.send_message(ID, "[id{0}|{1} {2}], отъебись блять".format(mess['user_id'],
                                                                           user['first_name'],
                                                                           user['last_name']))
        if com in self.func_dict:
            try:
                f = self.func_dict[com]
                f(mess, ID)
            except Exception as e:
                self.bot.send_message(ID, "error: {0}".format(e.args))
                raise e
        if mess['user_id'] in self.greetings.keys():
            self.greet(mess, ID)

