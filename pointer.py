# -*- coding: utf-8 -*-

from url import getURLs
from name import url2name, path2urlList, getPageFileName
from cache import headRequestCached, getRequestCached, removeFromCache
from load import partialGetRequest
from head import isPage, isGoodStatus, getSize, isAcceptedPartialDownload
from path import checkPath

MAXFILESIZE = 1048576


class PointerHTTPFS():
    def __init__(self, root, path):
        self.root = root
        self.path = path
        self.isGoodStatus = False
        self.urllist, self.isPageFile = path2urlList(root, path)
        if checkPath(self.urllist):
            self.url = self.urllist[-1]
            self.resp = headRequestCached(self.url)
            if isGoodStatus(self.resp):
                self.isGoodStatus = True

    def isDir(self):
        if not self.isGoodStatus:
            return False
        return isPage(self.resp) and not self.isPageFile

    def isFile(self):
        if not self.isGoodStatus:
            return False
        return not isPage(self.resp) or self.isPageFile

    def getEntries(self):
        content = getRequestCached(self.url)
        urls = getURLs(content, self.url)
        urls = map(url2name, urls)
        urls = urls + [getPageFileName(self.url)]
        return urls

    def read(self, size, offset):
        if isPage(self.resp) or self.getSize() <= MAXFILESIZE:
            content = getRequestCached(self.url)
            slen = self.getSize()
            if offset < slen:
                if offset + size > slen:
                    size = slen - offset
                buf = content[offset:offset + size]
            else:
                raise RuntimeError("Invalid range")
        else:
            if isAcceptedPartialDownload(self.resp):
                buf = partialGetRequest(self.url, size, offset)
            else:
                raise RuntimeError("Not accepted partial download")
        return buf

    def release(self):
        if not isPage(self.resp):
            removeFromCache(self.url)

    def getSize(self):
        return getSize(self.resp)
