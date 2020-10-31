
from tools.wechat import WechatCharbot
from tools.dingtalk import DingtalkChatbot
import Config
import pysnooper

config = Config.Config()

def alertContent(msgDict):
    if 'alertTemplate' in msgDict:
        content = msgDict['alertTemplate'].format(**msgDict)
    elif msgDict.get('alertSource') == 'prometheus' and 'prometheus_template' in dir(config):
        content = config.prometheus_template.format(**msgDict)
    elif msgDict.get('alertSource') == 'prometheus' and 'prometheus_template' not in dir(config):
        msgDict.pop('alertStatus')
        msgDict.pop('distinct')
        msgDict.pop('alertSource')
        
        content =  'alertname: ' + msgDict['alertname'] + '\n'
        for key,value in msgDict.items():
            if key != 'alertname':
                content = content + '\n' + key + ': ' + str(value)
            
    elif 'template' in dir(config):
        content = config.template.format(**msgDict)
    else:
        content = 'alertname: ' + msgDict['alertname'] + '\n'
        content = content + '\n' + 'value: ' + msgDict['value']
        for key,value in msgDict.items():
            if key != 'alertname' or key != 'value':
                content =  content + '\n' + key + ': ' + str(value)   
    return content


def alertMethod(msgDict):
    
        if 'sendWechat' not in msgDict and config.sendWechat:
            msgDict['sendWechat'] = config.sendWechat
        if 'sendPhone' not in msgDict and config.sendPhone:
            msgDict['sendPhone'] = config.sendPhone
        if 'sendMail' not in msgDict and config.sendMail:
            msgDict['sendMail'] = config.sendMail
        if 'sendDingtalk' not in msgDict and config.sendDingtalk:
            msgDict['sendDingtalk'] = config.sendDingtalk
            
        content = alertContent(msgDict)
        
        if 'sendWechat' in msgDict:
            wechat = WechatCharbot()
            user =  msgDict['sendWechat'].replace(',','|').strip('|')
            wechat.sendto(user, content)
        
        if 'sendDingtalk' in msgDict:
            webhook = msgDict['sendDingtalk']
            dingtalk = DingtalkChatbot(config.webhook, secret=config.secretDingtalk, pc_slide=True)
            at_mobiles =  list(msgDict['atDingtalk'])
            dingtalk.sendto(content, at_mobiles)
            
@pysnooper.snoop()
def alertsend(msgDict):
    if 'alertSource' in msgDict and msgDict['alertSource'] == 'prometheus':
        alertMethod(msgDict)

    
    
    