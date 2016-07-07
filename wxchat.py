#!/usr/bin/env python
#encoding: utf-8

import os
import sys
import glob
import unicodedata
import sqlite3
import getopt

'''
{$HOME}/Library/Application Support/万达集团/万信/{wxuserid}/userdata.db

UserinfoTb:
    UserId,CnUserName,EnUserName,UserCode,Sex,Addr,Post,Tel,Phone,Email,PostCode,Fax,UpdateType,UpdateTime
'''

HOME = os.getenv('HOME', '/Users/*')

WX_PATH_PAT = HOME + r'/Library/Application Support/万达集团/万信/*/userdata.db'

def locate_db():

    dbpath = glob.glob(WX_PATH_PAT)

    if not len(dbpath):
        return False

    return dbpath[0]


def open_db(path):
    db = sqlite3.connect(path)
    return db.cursor()


def find_users(c, user, f):
    sql = "select %s from UserinfoTb u left join UserDeptInfoTb ud on ud.userid=u.userid left join DeptInfoTb d on d.deptid=ud.deptid where u.CnUserName like :key or u.EnUserName like :key or u.UserCode like :key or u.Tel like :key or u.Phone like :key or u.Email like :key order by u.UserCode" % f
    key = "%" + user + "%"
    c.execute(sql, {"key": key})
    return c.fetchall()


def width(s):
    if not s:
        return 0
    return sum([2 if unicodedata.east_asian_width(i) in 'WFA' else 1 for i in s])


def pad_field(s, w=0):
    ww = width(s)
    return (s if s else u'') + (' ' * (w - ww))


def pretty_print(users, f):
    fields = f.split(',')
    widths = [8] * len(fields)
    lwidths = len(widths)
    rwidths = range(lwidths)

    for i in xrange(len(users)):
        p = list(users[i])
        for j in rwidths:
            w = width(p[j]) + 2
            if widths[j] < w:
                widths[j] = w

        users[i] = p

    sys.stderr.write((u''.join([pad_field(fields[i], widths[i]) for i in rwidths])).encode('u8') + "\n")
    for u in users:
        sys.stdout.write((u''.join([pad_field(u[i], widths[i]) for i in rwidths])).encode('u8') + "\n")


def show_help():
    sys.stderr.write('Usage: %s {query}\n'.encode('u8'))
    sys.stderr.write('  {query}  Search keyword. Can be any of %s\n' % SEARCH_FIELDS)


def search_user(query, use_full):
    dbpath = locate_db()
    if not dbpath:
        return False

    fields_db, fields_cn = FIELDSET['full' if use_full else 'simple']
    cursor = open_db(dbpath)
    users = find_users(cursor, query, fields_db)

    return users


def search_chat(words):
    dbpath = locate_db()
    if not dbpath:
        return False

    cursor = open_db(dbpath)
    sql = "select isgroup, ssiontitle title, msgcontent, sendtime, userinfotb.cnusername username, usercode from MessageTb join userinfotb on sendid=userinfotb.userid join sessioninfotb on messagetb.ssionid=sessioninfotb.ssionid where %s order by sendtime desc limit 10"
    keys = dict((('key_%s' % i, u'%%%s%%' % words[i]) for i in xrange(len(words))))
    where = ' and '.join(("Msgcontent like :key_%s" % i for i in xrange(len(words))))
    import time

    chats = cursor.execute(sql % where, keys)
    #return chats.fetchall()
    return [[c[1],
             c[2],
             unicode(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(c[3])))),
             c[4],
             c[5]
             ] for c in chats.fetchall()]

    return [{"title": c[1].encode('utf8') if int(c[0]) else None,
             'content': c[2].encode('utf8'),
             'time': time.asctime(time.localtime(int(c[3]))),
             'sender': c[4].encode('utf8'),
             'sender_id': c[5]
             } for c in chats.fetchall()]


def main():
    chats = search_chat([w.decode('u8') for w in sys.argv[1:]])
    if chats == False:
        sys.stderr.write('Open Db Failed.')
    else:
        #sys.stdout.write(chats)
        print chats
        fields = u'讨论组,内容,发送时间,发言人,id'
        pretty_print(chats, fields)


if __name__=='__main__':

    main()
