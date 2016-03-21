#encoding: utf8
import sys
import workflow
import wxcontact as wx


def main(wf):

    query = wf.args[0]
    users = wx.search_user(query, True)

    if users == False:
        raise Exception('Open wanxin userdata.db failed')
        #wf.add_item("ERROR: Open wanxin userdata.db failed")
    elif not users:
        wf.add_item(u'Not found "%s"' % query)
    else:
        # 0      1      2    3    4    5    6    7    8
        #'中文名,英文名,代码,性别,职位,电话,手机,邮件,地址'
        [wf.add_item(
            "%s %s (%s) %s" % (u[0], u[1], u[2], u[4]), 
            "%s %s %s %s" % (u[6], u[5], u[7], u[8]),
            copytext='%s %s %s %s' % (u[2], u[6], u[5], u[7]),
            arg=u'%s %s\n手机: %s\n电话: %s\n邮箱: %s\n地址: %s' % (u[0], u[2], u[6], u[5], u[7], u[8]),
            uid=u[2],
            valid=True,
            icon="female.png" if u[3] == '0' else 'male.png'
            )
            for u in users[:100]]


    wf.send_feedback()


if __name__ == '__main__':
    wf = workflow.Workflow()
    sys.exit(wf.run(main))
