
from tools import WechatCharbot,DingtalkChatbot
import Config

wechat = WechatCharbot()
#dingtalk = DingtalkChatbot(webhook, secret=secret, pc_slide=True)
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


def alertMethod():
        pass

def alertSent(msgDict):
    if 'alertSource' in msgDict and msgDict['alertSource'] == 'prometheus':
        #msgDict['alertType'] = msgDict['distinct']
        alertContent(msgDict)
    #template = config.template
    #alertMsg = template.format(**d)
    
    
    