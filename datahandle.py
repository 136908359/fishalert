from ast import literal_eval
import datetime
from db import fiMongo
import logging,pysnooper
from fishconfig import fishConfig
from tools.logger import logger

fiMongo = fiMongo()
mongo = fiMongo.conn()


def intoMongo(data, source):
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
            logger.debug('Data from promeData, start to apply th rules, dataList is ' + str(dataList))      
            fishconfig = fishConfig(di)
            fishconfig.work()  
        
            
    elif isinstance(dataFormat, dict):
        dataFormat['alertStatus'] = 0
        dataFormat['alertAt'] = timeNow
        dataFormat['alertSource'] = source if 'alertSource' not in dataFormat else dataFormat['alertSource']
        
        dataList.append(dataFormat)
        logger.debug('Data from fishData, start to apply th rules, dataList is ' + str(dataList))
        fishconfig = fishConfig(dataFormat)
        fishconfig.work()

    else:
        pass
    
    result = mongo.alertmsg.insert_many(dataList).inserted_ids
    if isinstance(result, list):
        logger.debug('Insert success: {dataList}'.format(dataList = str(dataList)))
        return True
    else:
        logger.debug('Insert fail: {dataList}'.format(dataList = str(dataList)))
        return False
    


#发送告警后更新告警数据状态
def updateStatus(updDict):
    result = mongo.alertmsg.update_many(updDict)
    count = result.modified_count
    if count:
        msg = f'update success, the update data is {count}'
        logger.info(msg)    
        return True
    else:
        msg = 'update failure'
        logger.error(msg)
        return False