import datetime

testmsg='''
{
            "alertname":"PodMemoryUsage",
            "id":"/kubepods.slice/kubepods-besteffort.slice/kubepods-besteffort-podb6444dd6_a730_4029_98c7_f90b0819df1b.slice",
            "instance":"bluek8s11100node",
            "job":"kubernetes-cadvisor",
            "level":"1",
            "namespace":"id-prod-bluepay",
            "pod":"deployment-nas-1-7b9458674f-7wwtt",
            "type":"pod",
            "description":"kubernetes集群内deployment-nas-1-7b9458674f-7wwtt内存使用率超过80%(当前值: +Inf)",
            "summary":"内存使用率",
            "startsAt":"2020-09-11T08:12:09.994870056Z",
            "endsAt":"0001-01-01T00:00:00Z",
            "generatorURL":"http://prometheus-0:9090/graph?g0.expr=container_memory_rss%7Bcontainer%3D%22%22%2Cjob%3D%22kubernetes-cadvisor%22%2Cnamespace%3D%22id-prod-bluepay%22%7D+%2F+container_spec_memory_limit_bytes%7Bcontainer%3D%22%22%2Cjob%3D%22kubernetes-cadvisor%22%2Cnamespace%3D%22id-prod-bluepay%22%7D+%2A+100+%3E+80&g0.tab=1"
    }
'''

msg1='''
    {
        "labels":{
            "alertname":"PodMemoryUsage",
            "id":"/kubepods.slice/kubepods-besteffort.slice/kubepods-besteffort-podb6444dd6_a730_4029_98c7_f90b0819df1b.slice",
            "instance":"bluek8s11100node",
            "job":"kubernetes-cadvisor",
            "level":"1",
            "namespace":"id-prod-bluepay",
            "pod":"deployment-nas-1-7b9458674f-7wwtt",
            "type":"pod"
        },
        "annotations":{
            "description":"kubernetes集群内deployment-nas-1-7b9458674f-7wwtt内存使用率超过80%(当前值: +Inf)",
            "summary":"内存使用率"
        },
        "startsAt":"2020-09-11T08:12:09.994870056Z",
        "endsAt":"0001-01-01T00:00:00Z",
        "generatorURL":"http://prometheus-0:9090/graph?g0.expr=container_memory_rss%7Bcontainer%3D%22%22%2Cjob%3D%22kubernetes-cadvisor%22%2Cnamespace%3D%22id-prod-bluepay%22%7D+%2F+container_spec_memory_limit_bytes%7Bcontainer%3D%22%22%2Cjob%3D%22kubernetes-cadvisor%22%2Cnamespace%3D%22id-prod-bluepay%22%7D+%2A+100+%3E+80&g0.tab=1"
    }
'''

#fish = fishRules(fishconfig)
#fish.sendTo()
#fish.alertmsg()
'''
#解析每行配置
import re
fishd = {}
def fishline(line):
    for i in line.split("and"):
        expr = i.strip()
        #er)
        if re.match('{alertname}',expr):
            fishd['alertname'] =  expr.split('==')[1].strip()
        elif re.match('distinct', expr):
            distinct = expr.split(':')[1].strip()
        elif re.match('label', expr):
            label = expr.split(':')[1].strip() 
        else:
            print(expr)
'''
def get_alertname(file):
    with open(file,'r') as f:
        print(f.read())
        for line in  f.readlines():
            print(line)

#get_alertname('fishalert.conf')


#{alertname} -----> alertname的值

#str1 = '{alertname} == "test"'
#alertname = "test"
#newstr = re.sub('{alertname}', 'alertname', str1)
#print(newstr)
#print(eval(newstr))




from db import fiMongo

fiMongo = fiMongo()
mongo = fiMongo.conn()
#print(mongo.test.find_one())


def j(a):
    return a

str1 = 'j(a) > 100'

#locals()['a'] = 99
#print(eval(str1))


class test():
    def __ini__(self):
        pass
    def fun(self):
        return '111'
    def a(self):
        print(eval('self.fun()'))
    
#test = test()
#print(test.a())


str2 = 'hour() > 1 and hour() < 23'
import re
#print(re.findall('(?<= ?)\w+(?=\()',str2))


""" from flask import request
from flask import Flask
import json
app = Flask(__name__)
@app.route('/promeData', methods=['POST', 'GET'])
def echo():
    print(request.data)
    return '1'
    #print json.dumps(request.form) 
    #return True

if __name__ == '__main__': 
    app.run('0.0.0.0',8001)"""

""" import json
from ast import literal_eval
msg1 = json.loads(msg1)
msg1.update(msg1['annotations'])
msg1.update(msg1['labels'])
msg1.pop('annotations')
msg1.pop('labels')
msg1.pop('startsAt')
msg1.pop('endsAt')
msg1.pop('generatorURL') """




template = '告警主题: {alertname}\n告警值: {value}\n告警类型: {alertType}\n告警时间: {alertAt}\n告警来源: {alertSource}'

d = {'alertname': 'usage_90','alertType': ['pod','node'],'alertAt': '2020-10-26','alertSource':'prometheus'}

import re
for vari in re.findall('{(\S+)}', template):
    print(type(vari),d['alertname. '])
    print(template.format(vari=d['\''+vari+'\'']))
    





