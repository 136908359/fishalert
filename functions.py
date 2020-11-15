#统计周期内符合查询条件的记录数量，时间单位：秒
def count(self, seconds):
    queryDict = dict()        
    queryDict['alertStatus'] = 0
    queryDict['alertname'] = self.alertname
    
    if 'distinct' in fishConfig.assign(self):
        distincts = fishConfig.assign(self)['distinct']        
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
    
    if 'distinct' in fishConfig.assign(self):
        distincts = fishConfig.assign(self)['distinct']        
        for key in iter(distincts):
            try:
                queryDict[key] = self.msgDict[key]
            except KeyError as err:
                msg = 'fishrules: {} is not exists!'.format(key)
                logger.error(msg)
                
    fimongo = fiMongo()
    mongo = fimongo.conn()
    
    count = mongo.alertmsg.count_documents(queryDict)
    logger.debug('Notexists: the count of same message is ' + str(count))
    return True if count == 0  else False

def work(self):
    if self.flag:
        if self.match() and self.calculate():
            logger.debug('Work: match success')
            msgDict = self.assign()
            result = alertsend(msgDict)
            if result:
                return True
                
        else:
            logger.debug('Work: the message is not match the rule')
    else:
        logger.debug('Work: no rules match the message')
        