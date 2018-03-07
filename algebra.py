#!/usr/bin/python3
# -*- coding: utf-8 -*-

import collections
import math


def factorize(i):
    if i > 10**30:
        raise Exception("Number too big")
    factors = collections.deque()
    divisor = 2
    sq = math.sqrt(i)
    while divisor <= sq:
        while i % divisor == 0:
            i = int(i / divisor)
            factors.append(divisor)
            sq = math.sqrt(i)
        if divisor == 2:
            divisor -= 1
        divisor += 2
    if i != 1:
        factors.append(i)
    return [i for i in factors]


def gcdext(a, b):

    def gcdext_in(a, b):
        if a > 10**50 or b > 10**50:
            raise Exception("Number too big")
        if b == 0:
            return a, 1, 0
        d, x, y = gcdext_in(b, a % b)
        return d, y, x-math.floor(a/b)*y

    return [i for i in gcdext_in(a, b)]
