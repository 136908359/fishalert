from queue import Queue
from threading import Thread
from db import fiMongo
import time,sys,datetime
from ruleparser import ruleParser
from alert import alertSend
from datahandle import updateStatus
from tools.logger import logger

fiMongo = fiMongo()
mongo = fiMongo.conn()


class msghandle(object):
    
    def __init__(self):
        self.timerShort = Thread(name='timerShort', target=self.scan(5))
        self.timerLong = Thread(name='timerLong', target=self.scan(60))
        
    def scan(self, period):
        while True:
            timeline = (datetime.datetime.now()-datetime.timedelta(seconds=period)).strftime('%Y-%m-%d %H:%M:%S')
            for msgDict in mongo.alertmsg.find({'alertStatus': 0, 'alertAt': {'$gte': timeline }}):
                msg = f'discovery alert message: {msgDict}'
                logger.debug(msg)
                
                ruleparser = ruleParser(msgDict)
                if ruleparser.judge()[0]:
                    msgDict = ruleparser.judge()[1]
                    result = alertSend(msgDict)
                    if result:
                        updDict = {key:value for key,value in msgDict.items() if key in ['alertname','alertStatus']}
                        distincts = msgDict.get('distincts')
                        if distincts:
                            for key in distincts:
                                updDict[key] = msgDict.get(key) 
                        updateStatus(updDict)
                        
            time.sleep(period)        
                    
    def run(self):
        self.timerShort.run()
        
def main():
    handle = msghandle()
    handle.scan(5)
        
if __name__ == '__main__':
    main()  