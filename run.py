from multiprocessing import Process,Manager
import time,sys

from fishconfig import fishConfig
from tools.logger import logger
from tools.parser import dbParser,baseParser,alertParser

from api import app



def fishProcess(aq):
    host = baseParser.get('listenHost', '0.0.0.0')
    port = baseParser.getint('listenPort', 5000) 
    app.run(host=host, port=port)

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