
'''
解析fishalert告警规则配置文件fishalert.conf
配置文件同一个alertname不能重复，若出现重复，以最后一个为准
调用：
    fishconfig = fishConfig('nodeUnreach')
    fishconfig.conditions

'''
import re,datetime
from exception import ruleError
from db import fiMongo
import logging,traceback,sys

class fishConfig(object):
    
    file = 'fishalert.conf'

    def __init__(self, **msgDict):
        self.msgDict = msgDict
        self.alertname = msgDict['alertname'].strip()
        configDict = fishConfig.init(self)
        self.flag = True if self.alertname  in configDict else False        #alertname是否存在规则的标记
        self.conditions = configDict[self.alertname]['conditions']
        self.assignments = configDict[self.alertname]['assignments']
        self.functions = configDict[self.alertname]['functions']

    #初始化fishalert告警规则配置文件，返回解析后的配置文件字典
    def init(self):
        configDict = dict()

        with open(self.file, 'r') as f:
            for line in  f.readlines():
                if line.isspace():
                    continue
                
                conditions, tempList, assignments, functions = list(), list(), dict(), list()
                for expr in line.split('and'):
                    if re.match('^{alertname}', expr):
                        alertname = expr.split('==')[1].strip().strip('\'')
                    elif re.match('.+\(.*\).*', expr):
                        functions.append(expr.strip())
                    elif re.match('.*[=!<>].*', expr) and re.match('((?!alertname).)*', expr):
                        conditions.append(expr.strip())
                    elif re.match('.*:.*', expr):
                        tempList.append(tuple(expr.strip().split(':')))
                    else:
                        raise ruleError(expr)
                
                    assignments = { key:value.strip().split(',') for key,value in tempList }
                    tempDict = dict()                   
                    tempDict['conditions'] = conditions         #匹配
                    tempDict['assignments'] = assignments       #赋值
                    tempDict['functions'] = functions           #函数计算
                    configDict[alertname] = tempDict
                    
            return configDict

    def match(self):
        objExp = ' and '.join(self.conditions)
        for expr in self.conditions:
            for key in re.findall('{(.*?)}', expr):
                objExp = re.sub(r'{%s}' % key, key, objExp)
                if key in self.msgDict:
                    locals()[key] = self.msgDict[key]
        return eval(objExp)

    def assign(self):
        self.msgDict.update(self.assignments)
        return self.msgDict
        
    def calculate(self):        
        express = ' and '.join(self.functions)
        for vari in set(re.findall('\w+(?=\()',express)):
            express = express.replace(vari, 'self.' + vari)
        return eval(express)

    #统计周期内符合查询条件的记录数量，时间单位：秒
    def count(self, seconds):
        queryDict = dict()        
        queryDict['status'] = 0
        queryDict['alertname'] = self.alertname
        
        if 'distinct' in fishConfig.assign(self):
            distincts = fishConfig.assign(self)['distinct']        
            for key in iter(distincts):
                try:
                    queryDict[key] = self.msgDict[key]
                except KeyError as err:
                    msg = 'fishrules: {} is not exists!'.format(key)
                    logging.error(msg)
                    
        timeNow = datetime.datetime.now()
        timeTuple = timeNow - datetime.timedelta(seconds=seconds)
        timeThreshold = timeTuple.strftime('%Y-%m-%d %T')
        queryDict['alertAt'] = { '$gte': timeThreshold }             #系统自动生成alertAt字段

        fimongo = fiMongo()
        mongo = fimongo.conn()

        count = mongo.alertmsg.count_documents(queryDict)
        return count
    
    #输出当前时间，仅小时
    def hour(self):
        hourNow = datetime.datetime.now().hour
        return hourNow
    
    #告警收敛，根据告警级别
    def notexists(self, queryDict):
        queryDict['status'] = 0 
        
        if 'distinct' in fishConfig.assign(self):
            distincts = fishConfig.assign(self)['distinct']        
            for key in iter(distincts):
                try:
                    queryDict[key] = self.msgDict[key]
                except KeyError as err:
                    msg = 'fishrules: {} is not exists!'.format(key)
                    logging.error(msg)
                    
        fimongo = fiMongo()
        mongo = fimongo.conn()
        
        count = mongo.alertmsg.count_documents(queryDict)
        if count == 0:
            return True
        else:
            return False
        
    def work(self):
        if self.flag:
            if self.match() and self.calculate():
                msgDict = self.assign()
                alertSent(**msgDict)
            
            
        
        
        
        
        


def main():        
    msgDict = {'alertname':'cpuUsage_80','namespace':'id-test','idc':'inet','node':'sz-k8s'}

    fishconfig = fishConfig(**msgDict)
    #print(fishconfig.conditions)
    print(fishconfig.calculate())



if __name__ == '__main__':
    main()                    




