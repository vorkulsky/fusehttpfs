# -*- coding: utf-8 -*-

from name import path2urlList
from cache import headRequestCached, getRequestCached
from head import isPage, isGoodStatus
from url import getURLs


def checkPath(path):
    d = len(path)
    for i in xrange(0, d - 1):
        resp = headRequestCached(path[i])
        if isGoodStatus(resp) and isPage(resp):
            content = getRequestCached(path[i])
            urls = getURLs(content, path[i])
            if path[i + 1] not in urls:
                return False
        else:
            return False
    return True
