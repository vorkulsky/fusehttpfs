#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno
import os
import stat
import sys

import fuse
from fuse import Fuse

from pointer import PointerHTTPFS

DEBAG = True

fuse.fuse_python_api = (0, 2)


class HTTPFS(Fuse):

    def __init__(self, root, *args, **kw):
        Fuse.__init__(self, *args, **kw)
        self.root = root
        if DEBAG:
            _debug('-' * 27 + ' mount ' + '-' * 27 + '\n')

    def getattr(self, path):
        if DEBAG:
            _debug('getattr: ' + path + '\n')
        st = StatHTTPFS()
        pt = PointerHTTPFS(self.root, path)
        if pt.isDir():
            st.st_mode = stat.S_IFDIR | 0444
            st.st_nlink = 2
        elif pt.isFile():
            st.st_mode = stat.S_IFREG | 0444
            st.st_nlink = 1
            st.st_size = pt.getSize()
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        if DEBAG:
            _debug('readdir: ' + path + '\n')
        pt = PointerHTTPFS(self.root, path)
        for entry in pt.getEntries():
            yield fuse.Direntry(entry)

    def open(self, path, flags):
        if DEBAG:
            _debug('open: ' + path + '\n')
        pt = PointerHTTPFS(self.root, path)
        if pt.isFile():
            accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
            if (flags & accmode) != os.O_RDONLY:
                return -errno.EACCES
        else:
            return -errno.ENOENT

    def read(self, path, size, offset):
        if DEBAG:
            _debug('read: ' + path + (' size:%d offset:%d' \
                                        % (size, offset)) + '\n')
        pt = PointerHTTPFS(self.root, path)
        try:
            return pt.read(size, offset)
        except RuntimeError, e:
            return -errno.EIO

    def release(self, path, flags):
        if DEBAG:
            _debug('release: ' + path + '\n')
        pt = PointerHTTPFS(self.root, path)
        pt.release()


class StatHTTPFS(fuse.Stat):
    def __init__(self):
        fuse.Stat.__init__(self)
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0


def _debug(s):
    f = open('/tmp/httpfs.log', 'a')
    f.write(s)
    f.close()


def main():
    baseurl = ''
    if len(sys.argv) < 3:
        sys.argv += ['--help']
    else:
        baseurl = 'http://' + sys.argv[1]
        pt = PointerHTTPFS(baseurl, '/')
        if not pt.isDir():
            print 'Error: bad BaseURL\n'
            sys.argv += ['--help']

    usage = """%prog [BaseURL] [mountpoint] [options]"""

    server = HTTPFS(baseurl, version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')

    server.parse(errex=1)
    server.main()


if __name__ == '__main__':
    main()
