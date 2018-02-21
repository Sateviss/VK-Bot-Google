#!/usr/bin/python3
# -*- coding: utf-8 -*-

from threading import Thread
import time


def sosat(name, delay):
    for i in range(100):
        time.sleep(delay)
        print(time.ctime(time.time()), name)



# Create new threads
threads = []
names = ['kek', 'lol', 'karvalol']
for i in names:
    t = Thread(target=sosat, args=(i, 0.5))
    t.start()