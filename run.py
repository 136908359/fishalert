from flask import Flask
from flask import request
from flask import render_template
from flask_restful import Api,Resource,reqparse
from alertapi import alertData,login
from multiprocessing import Process,Manager
import db,alert,Config
import time
import sys

config = Config.Config()
fidb = db.fiDB()

def fishProcess(aq):

    app = Flask(__name__)

    api = Api(app)
    api.add_resource(alertData, '/alertdata')
    api.add_resource(login, '/login')

    app.run(host=config.listenHost, port=config.listenPort)

def cookProcess(aq):
    pass

def eatProcess():


    SQL = 'select * from alertmsg where status=0;'
    while True:
        data = fidb.Select(SQL)
        for index, item in enumerate(data):
            alert.alertRules(item)
        time.sleep(3)

def main():

    pfish = Process(target=fishProcess, args=(aq,))
    cfish = Process(target=cookProcess, args=(aq,))
    efish = Process(target=eatProcess, args=())
    pfish.start()
    cfish.start()
    efish.start()
    pfish.join()




if __name__ == '__main__':
    manager = Manager()
    aq = manager.dict()
    main()
