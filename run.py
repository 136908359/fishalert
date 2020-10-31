from flask import Flask
from flask import request
from flask import render_template
from flask_restful import Api,Resource,reqparse
from alertapi import alertData,login,promeData
from multiprocessing import Process,Manager
import db,alert,Config
import time,sys
from datahandle import intoMongo 
from fishconfig import fishConfig
from tools.logging import logger


app = Flask(__name__)
config = Config.Config()

@app.route('/promeData', methods=['POST', 'GET'])
def promeData():
    data = request.data
    logger.debug('Accept the data' + str(data))
    result = intoMongo(data)
    
    if result:
        return 'Insert success'
    else:
        return 'Insert failure'

def fishProcess(aq):    
    app.run(host=config.listenHost, port=config.listenPort)

def cookProcess(aq):
    pass

def eatProcess():
    pass

def main():

    pfish = Process(target=fishProcess, args=(aq,))
    #cfish = Process(target=cookProcess, args=(aq,))
    efish = Process(target=eatProcess, args=())
    pfish.start()
    #cfish.start()
    efish.start()
    pfish.join()




if __name__ == '__main__':
    manager = Manager()
    aq = manager.dict()
    main()