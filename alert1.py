import db,Config
import pysnooper
from tools import DingtalkChatbot,WechatCharbot
import logging
import sys,json,re
import rules

fidb = db.fiDB()
config = Config.Config()

#更新告警模板的变量，输出完整的告警内容
def setTemplate(**kw):
   #如果列表中custom_template存在，则把custom_template当做模板
   if kw.get('custom_template'):
      template = kw.get('custom_template')
      return template
   template = kw.get('template')
   mecos = re.findall('{{\S+}}', template)  # 变量名不能非单词的字符
   for index, item in enumerate(mecos):
      varia = re.sub('\W', '', item)
      if kw.get(varia):
         template = template.replace(item, str(kw.get(varia)))  # 若变量存在，将模板变量替换
   return template


#告警发送成功后，更新alertmsg表的告警状态为 1
#告警策略阻拦后，更新alertmsg表的告警状态为 2
def statusUpd(id,status):
   SQL = 'update alertmsg set status = {} where id=\"{}\"'.format(status,id)
   data = fidb.Update(SQL)
   if not data:
      msg = 'Sql update success: (id, status) values ({}, {})'.format(id, status)
      logging.warning(msg)
      return True


#输入全部参数，发送告警
def sendMsg(**kw):
   #ruleJug(**kw)
   #sys.exit(1)
   if not rules.ruleJug(**kw):
      msg = 'Alarm rule is refuse: (id, alertname, rule) values ({}, {}, {})'.format(kw.get('alertmsg_id'),kw.get('alertname'),kw.get('rule'))
      logging.warning(msg)
      statusUpd(kw.get('alertmsg_id'),2)
      return False
   wechat = WechatCharbot()

   varias = kw.copy()
   sendway = varias.get('sendway')

   if sendway == 'wechat':
      users = varias.get('sendto').replace(',', '|')
      msg = setTemplate(**varias)
      result = wechat.sendto(users, msg)
      if result:
         alertmsg_id = varias.get('alertmsg_id')
         statusUpd(alertmsg_id,1)
         msg = 'Alarms sent completed:  (id, alertname) values (' + str(varias.get('alertmsg_id')) + ',' + varias.get('alertname') + ')'
         logging.warning(msg)

   elif sendway == 'dingtalk':
      msg = ''
      for index, webhook in enumerate(sendto.split(',')):
         dingtalk = DingtalkChatbot(webhook, secret=secret, pc_slide=True)
         dingtalk.sendto(msg, at_mobiles=at_mobiles)
   elif sendway == 'phone':
      pass
   else:
      msg = 'Sendway: ' + sendway + ' is not exists. '
      # logging.warnning(msg)

#输入alertmsg表的参数，构造所需的所有参数
def setMsgData(**kw):

   # 去除表alertmsg与表media重复的字段
   kw['alertmsg_id'] = kw['id']
   kw['alerttime'] = kw['createtime']
   kw['alertmsg_updatetime'] = kw['updatetime']
   kw.pop('id')
   kw.pop('createtime')
   kw.pop('updatetime')


   #指定默认告警模板与媒介
   kw['sendway'] = config.sendway
   kw['sendto'] = config.sentto
   kw['template'] = config.template

   varias = kw.copy()
   # 整合告警模板、告警媒介与告警消息，输出一个包含所有需要的参数的字典
   for key in json.loads(varias.get('variable')):
      varias[key] = json.loads(varias.get('variable'))[key]


   SQL = 'select m.*,t.template from template as t left join tm on t.alertname=tm.alertname left join media as m on tm.medianame=m.medianame where tm.id is not NULL and  m.id is not NULL and t.alertname=\"{}\";'.format(kw.get('alertname'))
   data = fidb.Select(SQL)

   #当alertname在template与media表中不存在，使用默认的模板与媒介发送告警；
   #当alertname在template与media表中存在，使用template与media表中的配置发送告警
   if not data:
      sendMsg(**varias)
   else:
      for index, item in enumerate(data):
         #去除空value，避免空值覆盖了默认值
         for key in list(item.keys()):
            if not item[key]:
               del item[key]
         varias.update(item)

         # 自定义变量优先级最高
         for key in json.loads(varias.get('variable')):
            varias[key] = json.loads(varias.get('variable'))[key]
         sendMsg(**varias)
         #rules.ruleJug(**varias)



def alertRules(item):
   id = item.get('id')
   alertname = item.get('alertname')
   value = item.get('value')
   source = item.get('source')
   createtime = item.get('createtime')
   variable = json.loads(item.get('variable','{}'))
   names = locals().pop('item')

   setMsgData(**names)


if __name__ == '__main__':
   main()