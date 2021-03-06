#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
import glob
import getopt
import hashlib
import wx
import workflow

base_dir = wx.USER_CONFIG['DOWN_DIR'].encode('u8')
applog_dir = wx.APP_CONFIG['APP_DIR'] + '/AppLogs'
wf = workflow.Workflow()

def pformat(n):
    return '{:,}'.format(n)


def any_in(keys, dic):
    for i in keys:
        if i in dic:
            return True


def get_options(args):
    args, files = getopt.getopt(args, "Aaid", ["all", "img", "dup"])

    args = dict(args)

    result = {
            'img': None,
            'dup': None,
            'all': None,
            }

    if any_in(['-i', '--img'], args):
        result['img'] = True

    if any_in(['-d', '--dup'], args):
        result['dup'] = True

    if any_in(['-a', '--all'], args):
        result['img'] = True
        result['dup'] = True

    if any_in(['-A'], args):
        result['all'] = True

    return result


def ask_user(prompt_words):
    return False


def fuck_all():
    c = 0
    t = 0
    ts = 0

    for f in glob.iglob(base_dir + '/*'):
        try:
            fstat = os.stat(f)
            fsize = fstat.st_size
        except:
            fsize = 0

        t += 1
        try:
            os.unlink(f)
            c += 1
            ts += fsize
        except:
            pass

    import time
    now = time.time()

    for f in glob.iglob(applog_dir + '/*'):
        try:
            fstat = os.stat(f)
            fsize = fstat.st_size
            ftime = fstat.st_ctime
        except:
            fsize = 0
            ftime = now

        if ftime < now - 86400 * 2:
            try:
                os.unlink(f)
                c += 1
                ts += fsize
            except:
                pass

    #print ("%s %s %s %s\n%s %s" % (pformat(t), 'files found,', pformat(c), 'files deleted,', pformat(ts), "B disk space freed."))
    return (c, ts)

def fuck_images():
    c = 0
    t = 0
    ts = 0

    exts = ['[jJ][pP][gG]', '[bB][mM][pP]', '[pP][nN][gG]', '[gG][iI][fF]']
    for ext in exts:
        for f in glob.iglob(base_dir + '/*.' + ext):
            try:
                fstat = os.stat(f)
                fsize = fstat[6]
            except:
                fsize = 0

            t += 1
            try:
                os.unlink(f)
                c += 1
                ts += fsize
            except:
                pass

    #print ("%s %s %s %s\n%s %s" % (pformat(t), 'images found,', pformat(c), 'images deleted,', pformat(ts), "B disk space freed."))
    return (c, ts)


def fuck_duplicates():
    dc = 0
    ft = 0
    ts = 0
    hashes = {}

    for f in glob.iglob(base_dir + '/*.*'):
        try:
            fstat = os.stat(f)
            fsize = fstat[6]
        except:
            fsize = 0

        try:
            md5 = hashlib.md5()
            for l in open(f, 'r'):
                md5.update(l)
        except:
            continue

        h = md5.hexdigest()

        if h in hashes:
            ft += 1
            try:
                os.unlink(f)
                dc += 1
                ts += fsize
            except:
                pass
        else:
            hashes[h] = f

    return (dc, ts)


def fuck(options):
    dc = 0
    ts = 0

    if options['img']:
        result = fuck_images()
        dc += result[0]
        ts += result[1]

    if options['dup']:
        result = fuck_duplicates()
        dc += result[0]
        ts += result[1]

    if options['all']:
        result = fuck_all()
        dc += result[0]
        ts += result[1]

    if options['img'] or options['dup'] or options['all']:
        print ('清除 %s 个文件，\n释放 %sB 空间' % (pformat(dc), pformat(ts)))
    else:
        pass


def main():
    options = get_options(sys.argv[1:])
    fuck(options)


if __name__ == '__main__':
    main()
