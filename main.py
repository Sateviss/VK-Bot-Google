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

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        func = item[0]
        try:
            func(item[1])
        finally:
            q.task_done()


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
handle = Handler(marvin, safe_list)

q = queue.Queue()
threads = []
last_message = marvin.get_inbox()['mid']

for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.start()
    threads.append(t)

print("...working...")

a = sys.argv
if len(a) == 3:
    if a[1] == "update":
        marvin.send_message(a[2], "-обновление завершено-")

while 1:
    time.sleep(0.1)
    l_m = marvin.get_inbox()['mid']
    if l_m != last_message:
        q.join()
        inbox = marvin.get_inbox(last_message)
        last_message = l_m
        for m in inbox:
            q.put((handle.handle_message, m))
    i = 0
    while i < len(handle.nahui):
        if handle.nahui[i][1] < time.time():
            handle.bot.delete_message(handle.nahui[i][0])
            handle.nahui.pop(i)
            continue
        i += 1