
'''
解析fishalert告警规则配置文件fishalert.conf
配置文件同一个alertname不能重复，若出现重复，以最后一个为准
调用：
    fishconfig = fishConfig('nodeUnreach')
    fishconfig.conditions

'''
import re,datetime,json
from tools.exception import ruleError
from db import fiMongo
from alert import alertsend
import traceback,sys,pysnooper
from tools.logger import logger


class ruleParser(object):
    
    def __init__(self, msgDict):
        self.msgDict = msgDict
        self.alertname = self.msgDict.get('alertname')
        self.file = 'rules.conf'
        self.configDict = self.init()

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
                
                assignments = { key.strip():value.strip().split(',') for key,value in tempList }

                tempDict = dict()                   
                tempDict['conditions'] = conditions         #匹配
                tempDict['assignments'] = assignments       #赋值
                tempDict['functions'] = functions           #函数计算
                if alertname not in configDict:
                    configDict[alertname] = list()
                configDict[alertname].append(tempDict)
                    
            return configDict                 

    #在rules.conf中查找alertname
    #输出该alertname的所有rule，以列表的形式
    def get(self):

        result = self.configDict.get(self.alertname)
        if result:
            return result
        else:
            msg = 'ruleParser: %s is not exists.' % self.alertname  
            logger.debug(msg)
            return {}
        
    #返回ruleparser匹配的结果
    #判断满足条件返回true和处理后的msgDsict；否则返回false和{}
    def judge(self):
        matList = self.get()

        for i in range(len(matList)):
            di = matList[i]

            self.conditions = di.get('conditions')
            self.functions = di.get('functions')
            self.assignments = di.get('assignments')
            
            if self.match() and self.calculate():

                msgDict = self.assign()
                return (True, msgDict)
            else:
                continue
        
        return (False,{})
            
            
    #输入mongo中查找的告警消息conditions，输出匹配的True或False
    def match(self):
        if not self.conditions:
            return True

        objExp = ' and '.join(self.conditions)
        objExp = objExp.replace(r'{',r'"{').replace(r'}',r'}"')
        try:
            objExp = objExp.format(**self.msgDict)
        except KeyError:
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            msg = f'ruleParser: {exc_value} is not exists in msgDict'
            logger.error(msg)
            return False
        

        try:
            result = eval(objExp)
        except SyntaxError:
            msg = f'ruleParser: invalid syntax of eval() : {objExp}'
            logger.error(msg)
            return False
        else:
            return True if result is True else False


    #将匹配的rule的规则的assignments加入msgDict
    #输出rules规则扩展后的msgDict
    def assign(self):
        self.msgDict.update(self.assignments)                 #fishalert中的rules定义的label加入msgDict，且不覆盖msgDict原本的key
        return self.msgDict     

    #输入mongo中查找的告警消息functions，输出匹配的True或False
    def calculate(self):    
        if not self.functions:
            return True
        
        express = ' and '.join(self.functions)
        for vari in set(re.findall('\w+(?=\()',express)):
            express = express.replace(vari, 'self.' + vari)
        
        try:
            result = eval(express)
        except SyntaxError:
            msg = f'ruleParser: invalid syntax of eval() : {express}'
            logger.error(msg)
        else:
            return True if result is True else False

    #统计周期内符合查询条件的记录数量，时间单位：秒
    def count(self, seconds):
        queryDict = dict()        
        queryDict['alertStatus'] = 0
        queryDict['alertname'] = self.alertname
        
        if 'distinct' in self.assign():
            distincts =self.assign()['distinct']        
            for key in iter(distincts):
                try:
                    queryDict[key] = self.msgDict[key]
                except KeyError as err:
                    msg = 'fishrules: {} is not exists!'.format(key)
                    logger.error(msg)
                    
        timeNow = datetime.datetime.now()
        timeTuple = timeNow - datetime.timedelta(seconds=seconds)
        timeThreshold = timeTuple.strftime('%Y-%m-%d %T')
        queryDict['alertAt'] = { '$gte': timeThreshold }             #系统自动生成alertAt字段

        fimongo = fiMongo()
        mongo = fimongo.conn()

        count = mongo.alertmsg.count_documents(queryDict)
        logger.debug('Count: the count of conditions is ' + str(count) )
        return count
    
    #输出当前时间，仅小时
    def hour(self):
        hourNow = datetime.datetime.now().hour
        return hourNow
    
    #告警收敛，根据告警级别
    def notexists(self, queryDict):
        queryDict['alertStatus'] = 0
        
        if 'distinct' in self.assign():
            distincts = self.assign()['distinct']   
            for key in iter(distincts):
                try:
                    queryDict[key] = self.msgDict[key]
                except KeyError:
                    msg = 'ruleparser: {} is not exists!'.format(key)
                    logger.error(msg)
                    
        fimongo = fiMongo()
        mongo = fimongo.conn()
        
        count = mongo.alertmsg.count_documents(queryDict)
        logger.debug('Notexists: the count of same message is ' + str(count))
        return True if count == 0  else False
    
def main():
    ruleparser = ruleParser({"alertname":"cpuUsage_90","namespace":"id-test","idc":"inet"})
    print(ruleparser.judge())

if __name__ == '__main__':
    main()                    




