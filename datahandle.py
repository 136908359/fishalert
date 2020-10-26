from ast import literal_eval
import datetime
from db import fiMongo
import logging,pysnooper
from fishconfig import fishConfig

fiMongo = fiMongo()
mongo = fiMongo.conn()


#@pysnooper.snoop()
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
            
            di['alertStatus'] = 0
            di['alertAt'] = timeNow
            
            di['alertSource'] = 'prometheus' 
        
            dataList.append(di)
            fishconfig = fishConfig(**dataList)
            fishconfig.work()           
            
    elif isinstance(dataFormat, dict):
        if 'alertname' not in dataFormat:
            logging.warning('Alertname is none: {dataFormat}'.format(str(dataFormat)))
            return False
        
        dataFormat['status'] = 0
        dataFormat['alertAt'] = timeNow
        
        dataList.append(dataFormat) 
        fishconfig = fishConfig(**dataList)
        fishconfig.work()

    else:
        pass
    
    result = mongo.alertmsg.insert_many(dataList).inserted_ids
    if isinstance(result, list):
        logging.debug('Insert success: {dataList}'.format(dataList))
        return True
    else:
        return False
    
    
    