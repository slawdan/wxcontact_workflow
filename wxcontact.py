#!/usr/bin/env python
#encoding: utf-8

import os
import sys
import glob
import unicodedata
import getopt
import wx

'''
UserinfoTb:
    UserId,CnUserName,EnUserName,UserCode,Sex,Addr,Post,Tel,Phone,Email,PostCode,Fax,UpdateType,UpdateTime
'''

HOME = os.getenv('HOME', '/Users/*')

WX_PATH_PAT = HOME + r'/Library/Application Support/万达集团/万信/*/userdata.db'

FULL_FIELDS_CN = u'中文名,英文名,代码,性别,职位,电话,手机,邮件,地址,部门'
FULL_FIELDS    = u'u.CnUserName,u.EnUserName,u.UserCode,u.Sex,u.Post,u.Tel,u.Phone,u.Email,u.Addr,d.CnDeptName'
FIELDS_CN      = u'中文名,代码,性别,职位,电话,手机,邮件,部门'
FIELDS         = u'u.CnUserName,u.UserCode,u.Sex,u.Post,u.Tel,u.Phone,u.Email,d.CnDeptName'
SEARCH_FIELDS  = u'中文名,英文名,代码,电话,手机,邮件'

FIELDSET = {
        'full': (FULL_FIELDS, FULL_FIELDS_CN),
        'simple': (FIELDS, FIELDS_CN)
        }


def find_users(c, user, f):
    sql = "select %s from UserinfoTb u left join UserDeptInfoTb ud on ud.userid=u.userid left join DeptInfoTb d on d.deptid=ud.deptid where u.CnUserName like :key or u.EnUserName like :key or u.UserCode like :key or u.Tel like :key or u.Phone like :key or u.Email like :key order by u.UserCode" % f
    key = "%" + user + "%"
    c.execute(sql, {"key": key})
    return c.fetchall()


def trans_sexual(s):
    sexuals = {"1": u"男", "0": u"女"}
    return sexuals.get(s, u"")


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
        p[3] = trans_sexual(p[3])
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
    fields_db, fields_cn = FIELDSET['full' if use_full else 'simple']
    cursor = wx.open_userdata_db()
    users = find_users(cursor, query, fields_db)

    return users


def main():
    try:
        opts, q = getopt.getopt(sys.argv[1:], 'f')
        q = unicode(q[0], 'utf8')
    except:
        show_help()
        return

    opts = dict(opts)

    if opts.get('-f') is not None:
        fields_db, fields_cn = FIELDSET['full']
    else:
        fields_db, fields_cn = FIELDSET['simple']

    users = search_user(q, opts.get('-f') is not None)
    if users == False:
        sys.stderr.write('Open Db Failed.')
    else:
        pretty_print(users, fields_cn)


if __name__=='__main__':

    main()

