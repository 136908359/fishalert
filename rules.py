import db,Config,alerttype,alert
import re

fidb = db.fiDB()
config = Config.Config()

#策略1，rules支持带变量的表达式
def rule_express(**kw):
   SQL = 'select r.alertname,r.rule from alertmsg as a left join  rules as r on a.alertname = r.alertname where r.id is not null and a.alertname = \"{}\";'.format(kw.get('alertname'))
   data = fidb.Select(SQL)

   if data:
      kw['rule'] = data.get('rule') if kw.get('rule') is None else None

   #将rule转化为表达式
   rule = kw.get('rule','')

   mecos = re.findall('{{\S+}}', rule)
   for index, item in enumerate(mecos):
      varia = re.sub('\W', '', item)
      if kw.get(varia):
         rule = rule.replace(item, str(kw.get(varia,'')))

   if not rule:                  #rule不存在，立即告警
      return True
   elif eval(rule):              #根据表达式判断真假,表达式为真，立即告警
      alert.sendMsg(**kw)
   else:
      pass

def rule_similar(**kw):
   pass



def ruleJug(**kw):
   pass

if __name__ == '__main__':
   main()