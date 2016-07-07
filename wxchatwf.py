#encoding: utf8
import sys
import workflow
import wxchat as wx


def main(wf):

    words = wf.args
    chats = wx.search_chat(words)

    if chats == False:
        raise Exception('Open wanxin userdata.db failed')
    elif not chats:
        wf.add_item(u'Not found "%s"' % ' '.join(words))
    else:
        [wf.add_item(
            u"%s-%s %s %s" % (c[3], c[4], c[0], c[2]), 
            u"%s" % c[1],
            copytext=u"%s-%s(%s): %s" % (c[3], c[4], c[2], c[1]),
            arg=u"%s-%s(%s): %s" % (c[3], c[4], c[2], c[1]),
            #arg=u'%s %s\n手机: %s\n电话: %s\n邮箱: %s\n地址: %s' % (u[0], u[2], u[6], u[5], u[7], u[8]),
            valid=True,
            icon="wanxin.png"
            )
            for c in chats]

    wf.send_feedback()


if __name__ == '__main__':
    wf = workflow.Workflow()
    sys.exit(wf.run(main))
