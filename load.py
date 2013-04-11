# -*- coding: utf-8 -*-

import httplib2
import socket


def headRequest(url):
    timeout = 2
    h = httplib2.Http()
    socket.setdefaulttimeout(timeout)
    try:
        resp, content = h.request(url, 'HEAD')
    except IOError, e:
        resp = {}
    return resp


def getRequest(url):
    timeout = 2
    h = httplib2.Http()
    socket.setdefaulttimeout(timeout)
    try:
        resp, content = h.request(url, 'GET')
    except IOError, e:
        (resp, content) = ({}, '')
    return resp, content


def partialGetRequest(url, size, offset):
    timeout = 2
    h = httplib2.Http()
    socket.setdefaulttimeout(timeout)
    resp, content = h.request(url, 'GET', \
        headers={'range': 'bytes=%d-%d' % (offset, offset + size - 1)})
    return content
