# -*- coding: utf-8 -*-

import re
from urlparse import urlparse, urljoin

URL_RE = re.compile(r"""(?i)
<\s*
(?:a|area|img|link)
\s+[^>]*?
(?:href|src)
\s*=\s*
[\'\"]([^\'\"]+)
""", re.VERBOSE)

CACHE = {}


def isHTTP(url):
    o = urlparse(url)
    return o.scheme == '' or o.scheme == 'http'


def getURLs(content, base):
    if base in CACHE:
        return CACHE[base]
    # Поиск URL в тексте html-файла
    urls = URL_RE.findall(content)
    # Отбрасывание не HTTP URL
    urls = filter(isHTTP, urls)
    # Получение абсолютных адресов из относительных
    urls = map(lambda url: urljoin(base, url), urls)
    # Удаление дубликатов
    urls = list(set(urls))
    CACHE[base] = urls
    return urls
