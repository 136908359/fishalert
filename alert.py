
from tools import WechatCharbot,DingtalkChatbot
import Config

wechat = WechatCharbot()
dingtalk = DingtalkChatbot(webhook, secret=secret, pc_slide=True)
config = Config.Config()


def alertSent(**msgDict):
    if 'alertSource' in msgDict and msgDict['alertSource'] == 'prometheus':
        msgDict['alertType'] = msgDict['distinct']
    
    template = config.template
    
    
        