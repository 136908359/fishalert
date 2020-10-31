from ast import literal_eval
import datetime
from db import fiMongo
import logging,pysnooper
from fishconfig import fishConfig
from tools.logging import logger

fiMongo = fiMongo()
mongo = fiMongo.conn()


def intoMongo(data):
    dataList = list()
    timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dataFormat = literal_eval(str(data, encoding = "utf-8"))
    
    if isinstance(dataFormat, list):
        for di in dataFormat:
            
            di.update(di['annotations'])
            di.update(di['labels'])
            di.pop('annotations')
            di.pop('labels')
            di.pop('startsAt')
            di.pop('endsAt')
            di.pop('generatorURL')
            di.pop('id')   
            
            di['alertStatus'] = 0
            di['alertAt'] = timeNow
            
            di['alertSource'] = 'prometheus' if 'alertSource' not in di else di['alertSource']
            
            dataList.append(di)
            logger.debug('Data from prometheus, start to apply th rules, dataList is ' + str(dataList))      
            fishconfig = fishConfig(di)
            fishconfig.work()  
        
            
    elif isinstance(dataFormat, dict):
        if 'alertname' not in dataFormat:
            logger.warning('Alertname is none: {dataFormat}'.format(str(dataFormat)))
            return False
        
        dataFormat['alertStatus'] = 0
        dataFormat['alertAt'] = timeNow
        dataFormat['alertSource'] = 'sourceip' if 'alertSource' not in dataFormat else dataFormat['alertSource']
        
        logger.debug('Data from dict, start to apply th rules, dataList is ' + str(dataList))      
        dataList.append(dataFormat)
        #fishconfig = fishConfig(dataFormat)
        #fishconfig.work()
        

    else:
        pass
    
    result = mongo.alertmsg.insert_many(dataList).inserted_ids
    if isinstance(result, list):
        logger.debug('Insert success: {dataList}'.format(dataList = str(dataList)))
        return True
    else:
        logger.debug('Insert fail: {dataList}'.format(dataList = str(dataList)))
        return False
    
    
    