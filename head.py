# -*- coding: utf-8 -*-


def isPage(resp):
    if 'content-type' in resp:
        if resp['content-type'].find('text/html') != -1:
            return True
    return False


def isGoodStatus(resp):
    if 'status' in resp:
        if resp['status'].find('200') != -1:
            return True
    return False


def getSize(resp):
    return int(resp['content-length']) if 'content-length' in resp else 0


def isAcceptedPartialDownload(resp):
    if 'accept-ranges' in resp:
        if resp['accept-ranges'] == 'bytes':
            return True
    return False
