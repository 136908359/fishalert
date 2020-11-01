
from tools.wechat import WechatCharbot
from tools.dingtalk import DingtalkChatbot
import pysnooper
from tools.logger import logger
import copy
from tools.parser import dbParser,baseParser,alertParser


def alertContent(msgDict):
    if 'alertTemplate' in msgDict:
        content = msgDict['alertTemplate'].format(**msgDict)
    elif msgDict.get('alertSource') == 'prometheus' and 'prometheus_template' in alertParser:
        content = alertParser.get('prometheus_template').format(**msgDict)
    elif msgDict.get('alertSource') == 'prometheus' and 'prometheus_template' not in alertParser:
        msgDict.pop('alertStatus')
        msgDict.pop('distinct')
        
        alertDict = copy.deepcopy(msgDict)
        alertDict.pop('sendWechat')
        alertDict.pop('sendDingtalk')
        alertDict.pop('sendPhone')
        alertDict.pop('sendMail')
        alertDict.pop('atDingtalk')
        alertDict.pop('secretDingtalk')
        
        content =  'alertname: ' + alertDict['alertname']
        for key,value in alertDict.items():
            if key != 'alertname':
                content = content + '\n' + key + ': ' + str(value)
            
    elif 'template' in alertParser:
        content = alertParser.get('template').format(**msgDict)
    else:
        content = 'alertname: ' + msgDict['alertname'] + '\n'
        content = content + '\n' + 'value: ' + msgDict['value']
        for key,value in msgDict.items():
            if key != 'alertname' or key != 'value':
                content =  content + '\n' + key + ': ' + str(value)  
                
    
    logger.debug('alertContent: alert content is ' + content)
    return content

def alertMethod(msgDict):
    
        if 'sendWechat' not in msgDict and 'sendWechat' in alertParser:
            msgDict['sendWechat'] = alertParser.get('sendWechat')
        if 'sendPhone' not in msgDict and 'sendPhone' in alertParser:
            msgDict['sendPhone'] = alertParser.get('sendPhone')
        if 'sendMail' not in msgDict and 'sendMail' in alertParser:
            msgDict['sendMail'] = alertParser.get('sendMail')
        if 'sendDingtalk' not in msgDict and 'sendDingtalk' in alertParser:
            msgDict['sendDingtalk'] = alertParser.get('sendDingtalk')
            msgDict['atDingtalk'] = alertParser.get('atDingtalk')
            msgDict['secretDingtalk'] = alertParser.get('secretDingtalk')
            
        content = alertContent(msgDict)
        
        if 'sendWechat' in msgDict:
            wechat = WechatCharbot()
            user =  msgDict['sendWechat'].replace(',','|').strip('|')
            logger.debug('AlertMethod: send to wechat: user is {}'.format(user))
            wechat.sendto(user, content)
        
        if 'sendDingtalk' in msgDict:
            webhook = msgDict['sendDingtalk']
            secret = msgDict['secretDingtalk']
            atDingtalk = msgDict['atDingtalk']
            dingtalk = DingtalkChatbot(webhook, secret=secret, pc_slide=True)
            atDingtalk =  list(msgDict['atDingtalk']) if 'atDingtalk' in msgDict else []
            logger.debug('AlertMethod: send to dingtalk: webook is {},atDingtalk is {}'.format(webhook, atDingtalk))
            dingtalk.sendto(content, atDingtalk)
            
        if 'sendWechat' not in msgDict and 'sendDingtalk' not in msgDict and 'sendPhone' not in msgDict and 'sendMail' not in msgDict:
            logger.debug('AlertMethod: sendMethod is not match ')

def alertsend(msgDict):
    if 'alertSource' in msgDict and msgDict['alertSource'] == 'prometheus':
        alertMethod(msgDict)

    
    
    