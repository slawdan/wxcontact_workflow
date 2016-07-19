#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
import glob
import getopt
import hashlib
import wx

base_dir = wx.USER_CONFIG['DOWN_DIR']

def pformat(n):
    return '{:,}'.format(n)


def any_in(keys, dic):
    for i in keys:
        if i in dic:
            return True


def get_options(args):
    args, files = getopt.getopt(args, "aid", ["all", "img", "dup"])

    args = dict(args)

    result = {
            'img': None,
            'dup': None,
            }

    if any_in(['-i', '--img'], args):
        result['img'] = True
        result['dup'] = False

    if any_in(['-d', '--dup'], args):
        result['dup'] = True
        result['img'] = False

    if any_in(['-a', '--all'], args):
        result['img'] = True
        result['dup'] = True

    return result


def ask_user(prompt_words):
    return False


def fuck_images():
    c = 0
    t = 0
    ts = 0

    #for f in glob.iglob(base_dir + '/*.{[jJ][pP][gG],[bB][mM][pP],[pP][nN][gG],[gG][iI][fF]}'):
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
                print 'deleted image:', f
            except:
                print 'delete image failed:', f

    print '-' * 80
    print pformat(t), 'images found,', pformat(c), 'images deleted,', pformat(ts), "B disk space released."
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
            print 'calculate file digest failed:', f
            continue

        h = md5.hexdigest()

        if h in hashes:
            ft += 1
            try:
                os.unlink(f)
                dc += 1
                ts += fsize
                print 'deleted dup file:', f
            except:
                print 'delete dup file failed:', f
        else:
            hashes[h] = f

    print '-' * 80
    print pformat(ft), 'dup files found,', pformat(dc), 'files deleted,', pformat(ts), "B disk space released."
    return (dc, ts)


def fuck(options):
    dc = 0
    ts = 0

    img_confirmed = False
    if options['img'] == None:
        img_confirmed = ask_user('Clean images (png,jpg,gif,bmp)? [Y/n]')

    if img_confirmed or options['img']:
        result = fuck_images()
        dc += result[0]
        ts += result[1]

    dup_confirmed = False
    if options['dup'] == None:
        dup_confirmed = ask_user('Clean duplicate files? [Y/n]')

    if dup_confirmed or options['dup']:
        result = fuck_duplicates()
        dc += result[0]
        ts += result[1]

    if img_confirmed or options['img'] or dup_confirmed or options['dup']:

        print '=' * 80
        print 'Total', pformat(dc), 'files deleted,', pformat(ts), 'B disk space released.'
    else:
        print '''Usage: fuck_wanxin [options]
        \rShow usage.\n\r
        \rOptions:
        -i, --img   clean images.
        -d, --dup   clean duplicate files.
        -a, --all   clean all.
        '''


def main():
    options = get_options(sys.argv[1:])
    fuck(options)


if __name__ == '__main__':
    main()
