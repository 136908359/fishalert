import sys
sys.path.append("../")

#wechat
import pysnooper
import sys, json, re
import urllib.request as urllib2
import urllib
import Config

config = Config.Config()


class WechatCharbot(object):

    def __init__(self):
        self.CropID = 'ww68d301f8c4911662'
        self.Secret = 'YlZbgV_sGsD3a3jPDfM3S-LC12qcYWneHse1bhNkLY8'
        self.AppID = 1000002

    def sendto(self, users, Msg):
        # defaultencoding = 'utf-8'
        # if sys.getdefaultencoding() != defaultencoding:
        #     reload(sys)
        # sys.setdefaultencoding(defaultencoding)

        UserID = users
        GURL = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + self.CropID + '&corpsecret=' + self.Secret
        Request = urllib2.Request(GURL)
        Response = urllib2.urlopen(Request)
        access_token = eval(Response.read())['access_token']
        PURL = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
        data = {
            "touser": UserID,
            # "toparty": PartyID,
            "msgtype": "text",
            "agentid": self.AppID,
            "text": {
                "content": Msg
            },
            "safe": 0
        }

        encodeData = json.dumps(data, ensure_ascii=False).encode('utf-8')
        Request = urllib2.Request(PURL, encodeData)
        result = json.loads(str(urllib2.urlopen(Request).read(),'utf-8'))

        errcode = result['errcode']
        if not errcode:
            msg = 'Wechat message send to ' + users + ' success: ' + Msg
            #logging.debug(msg)
            return True
        else:
            errmsg = result['errmsg']
            msg = 'Wechat message send to ' + users + ' send failure: ' + errmsg
            #logging.warnning(msg)
            return False

if __name__ == '__main__':
    main()