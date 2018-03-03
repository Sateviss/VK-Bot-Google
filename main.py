#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import math
from threading import Thread

import os

from wrap import VkWrap
from handler import Handler
import queue
import random
import sys
import logging
import configparser

num_worker_threads = 4
logger = logging.Logger("VK-Bot")


safe_list = [math.acos, math.asin, math.atan, math.atan2, math.ceil, math.cos, math.cosh, math.degrees,
             math.exp, math.fabs, math.floor, math.fmod, math.frexp, math.hypot, math.ldexp, math.log, math.log10,
             math.modf, math.pow, math.radians, math.sin, math.sinh, math.sqrt, math.tan, math.tanh, random.randrange,
             int, str]

if not os.path.exists("config.ini"):
    print("config.ini does not exist, you must create one\n"
          "You can base your config on example_config.ini")
    sys.exit(1)

try:
    config = configparser.ConfigParser()
    config.read("config.ini")
    app_id = config['GENERAL']['App ID']
    if config['GENERAL'].getboolean('Use token'):
        marvin = VkWrap(key=config['VK TOKEN']['Access token'])
    else:
        marvin = VkWrap(login=config['VK LOGIN INFO']['Login'], password=config['VK LOGIN INFO']['Password'])
    google_api_key = config['API KEYS'].get('Google URL shortener API key', 'kek')
    handle = Handler(marvin, safe_list, logger, google_api_key)
except Exception as e:
    print("Something went wrong with config.ini\n"
          "Check if you have set it up correctly\n\n"
          "Here's the error: "+str(e.args))
    sys.exit(1)

# marvin.send_message(ID, "Бот Запущен")

q = queue.Queue()
threads = []


def worker():
    while True:
        item = q.get()
        if item is None:
            break
        func = item[0]
        try:
            q.task_done()
            func(item[1])
        except Exception as e:
            print(e)
            logger.exception('Got exception on worker Thread')


def deleter(hand: Handler, bot: VkWrap):
    while True:
        time.sleep(0.1)
        item = hand.nahui.get()
        if item[1] < time.time():
            bot.delete_message(item[0])
        else:
            hand.nahui.put(item)


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
        marvin.send_message(a[2], "обновление завершено")
        handle.changelog(mess=None, ID=a[2])

while 1:
    q.join()
    inbox = marvin.get_inbox_lp()
    for m in inbox:
        q.put((handle.handle_message, m))
