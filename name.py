# -*- coding: utf-8 -*-

SLASH = ' '
PREFIX = '[page] '


def name2url(name):
    return 'http://' + name.replace(SLASH, '/')


def url2name(url):
    name = url.replace('/', SLASH)
    name = name[7:]  # http://
    return name


def path2urlList(base, path):
    if path == '/':
        return ([base], False)
    urlList = path.split('/')
    pageFileBool = isPageFile(urlList[-1])
    if pageFileBool:
        urlList = urlList[:-1]
    urlList = [base] + map(name2url, urlList[1:])
    return (urlList, pageFileBool)


def isPageFile(name):
    return name.startswith(PREFIX)


def urlList2path(urlList, pageFileBool):
    urlList = map(url2name, urlList[1:])
    path = '/' + '/'.join(urlList)
    if pageFileBool:
        path += '/' + PREFIX + urlList[-1]
    return path


def getPageFileName(url):
    return PREFIX + url2name(url)
