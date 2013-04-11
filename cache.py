# -*- coding: utf-8 -*-

from load import headRequest, getRequest

CACHE = {}


def headRequestCached(url):
    if url in CACHE:
        resp, content = CACHE[url]
    else:
        resp = headRequest(url)
        content = ''
        if resp != {}:
            CACHE[url] = (resp, content)
    return resp


def getRequestCached(url):
    if url in CACHE:
        resp, content = CACHE[url]
        if content == '':
            resp, content = getRequest(url)
    else:
        resp, content = getRequest(url)
    CACHE[url] = (resp, content)
    return content


def removeFromCache(url):
    if url in CACHE:
        resp, content = CACHE[url]
        CACHE[url] = (resp, '')
