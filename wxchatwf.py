#encoding: utf8
import sys
import re
import workflow
import wxchat as wx


def santize_content(c):
    return re.sub(r'\s+', ' ', re.sub(r'<img.*?>', u'[图片]', c, flags=re.I))


def extract_image(c):
    res = re.search(r'<img\s.*?src="file:///(.*?)"', c, flags=re.I)
    return res.group(1) if res else None


def main(wf):
    words = wf.args
    chats = wx.search_chat(words)

    if chats == False:
        raise EnvironmentError('Open wanxin userdata.db failed')
    elif not chats:
        wf.add_item(u'Not found "%s"' % ' '.join(words))
    else:
        for c in chats:
            content = santize_content(c[1])
            text = u"%s-%s(%s):\n%s" % (c[3], c[4], c[2], santize_content(c[1]))
            icon = extract_image(c[1])
            wf.logger.warn(icon)

            wf.add_item(
                content,
                u"%s-%s %s %s" % (c[3], c[4], c[0], c[2]), 
                copytext=text,
                arg=text,
                icon=icon,
                valid=True
            )

    wf.send_feedback()


if __name__ == '__main__':
    wf = workflow.Workflow()
    sys.exit(wf.run(main))
