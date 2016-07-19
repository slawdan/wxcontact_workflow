# encoding: utf8
from os import path, stat
import time
import glob

import workflow
import wx

wf = workflow.Workflow()

def get_down_files():
    pat = wx.USER_CONFIG['DOWN_DIR'] + '/*'
    return [{'name': path.basename(f), 'filename': f, 'size': stat(f).st_size, 'time': stat(f).st_atime} for f in glob.iglob(pat)]


def key_for_file(f):
    return f['name']


def main(wf):
    files = wf.cached_data('wxfiles', get_down_files, max_age=5)
    filtered = wf.filter(wf.args[0], files, key_for_file, max_results=20, match_on=workflow.MATCH_ALL) if wf.args else files[:20]
    if filtered:
        [wf.add_item(
            n['name'],
            u"{1} ({0:,}字节) ".format(n['size'], time.strftime('%Y-%m-%d %H:%M', time.localtime(n['time']))),
            copytext=n['filename'],
            arg=n['filename'],
            valid=True
            )
            for n in filtered]
    else:
        wf.add_item(u'未找到文件', u'请确认文件是否存在，或者直接打开文件夹查找')
    wf.add_item(u'打开万信下载文件夹', copytext=wx.USER_CONFIG['DOWN_DIR'], arg=wx.USER_CONFIG['DOWN_DIR'], valid=True)


if __name__ == '__main__':
    main(wf)
    wf.send_feedback()
