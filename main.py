#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import math
from threading import Thread
from wrap import VkWrap
from handler import Handler
import queue
import random
import sys
import logging

logger = logging.Logger("VK-Bot")

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        func = item[0]
        try:
            func(item[1])
        except Exception as e:
            logger.exception('Got exception on worker Thread')
        finally:
            q.task_done()

def deleter(hand: Handler, bot: VkWrap):
    while True:
        time.sleep(0.1)
        item = hand.nahui.get()
        if item[1] < time.time():
            bot.delete_message(item[0])
        else:
            hand.nahui.put(item)

num_worker_threads = 4

file = open("login.txt", "r")
login = file.readline().replace('\n', '')
password = file.readline().replace('\n', '')
file.close()

marvin = VkWrap(login, password)

# marvin.send_message(ID, "---Бот Запущен---")

safe_list = [math.acos, math.asin, math.atan, math.atan2, math.ceil, math.cos, math.cosh, math.degrees,
             math.exp, math.fabs, math.floor, math.fmod, math.frexp, math.hypot, math.ldexp, math.log, math.log10,
             math.modf, math.pow, math.radians, math.sin, math.sinh, math.sqrt, math.tan, math.tanh, random.randrange,
             int, str]

handle = Handler(marvin, safe_list, logger)

q = queue.Queue()
threads = []
last_message = marvin.get_inbox()[0]['id']

t = Thread(target=deleter, args=(handle, marvin))
t.start()
threads.append(t)

for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.start()
    threads.append(t)

print("...working...")

a = sys.argv
if len(a) == 3:
    if a[1] == "update":
        marvin.send_message(a[2], "-обновление завершено-")
        handle.changelog(mess=None, ID=a[2])

while 1:
    q.join()
    inbox = marvin.get_inbox_lp()
    for m in inbox:
        q.put((handle.handle_message, m))