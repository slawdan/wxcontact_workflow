# encoding: utf8
import os
import glob
import sqlite3
import xml.etree.ElementTree as ET


APP_CONFIG = {
                'HOME_DIR': os.getenv('HOME'),
                'APP_DIR': u"/Library/Application Support/万达集团/万信",
                'LOGIN_DB': u"/user.db"
                }

USER_CONFIG = {
                'ID': '',
                'DIR': '',
                'DB': '/userdata.db',
                'CONFIG': '/UserConfig.xml',
                'DOWN_DIR': ''
                }


def open_db(path):
    db = sqlite3.connect(path)
    return db.cursor()


def init():
    if not APP_CONFIG['HOME_DIR']:
        home_pat = '/Users/*' 
        homes = glob.glob(home_pat)
        if not homes:
            raise EnvironmentError('Home dir not found')

        APP_CONFIG['HOME_DIR'] = homes[0]

    APP_CONFIG['APP_DIR'] = APP_CONFIG['HOME_DIR'] + APP_CONFIG['APP_DIR']
    APP_CONFIG['LOGIN_DB'] = APP_CONFIG['APP_DIR'] + APP_CONFIG['LOGIN_DB']

    c = open_db(APP_CONFIG['LOGIN_DB'])
    """CREATE TABLE LoginInfoTb(autologin,builtNum,cnname,database,enname,filedownload,fileupload,imagedownload,imageupload,logflag,loginid,logintype,loglevel,logodownload,logoupload,maxgroupmbrnum,newdofileupload,newfiledownload,newfileuploadget,p2pip,p2pport,psw,pswType,serverip,serveripb,serverport,serverportb,sex,state,usercode,version);"""
    c.execute("SELECT loginid from LoginInfoTb limit 1")
    l = c.fetchone()
    USER_CONFIG['ID'] = l[0]
    USER_CONFIG['DIR'] = APP_CONFIG['APP_DIR'] + '/' + USER_CONFIG['ID']
    USER_CONFIG['DB'] = USER_CONFIG['DIR'] + USER_CONFIG['DB']
    USER_CONFIG['CONFIG'] = USER_CONFIG['DIR'] + USER_CONFIG['CONFIG']

    tree = ET.parse(USER_CONFIG['CONFIG'])
    root = tree.getroot()
    USER_CONFIG['DOWN_DIR'] = root.find('downLoadPath').text

init()


def open_userdata_db():
    return open_db(USER_CONFIG['DB'])
