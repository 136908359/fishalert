from flask_restful import Api,Resource,reqparse
import pysnooper,time,json,socket
from tools.logger import logger

from flask import Flask
from flask import request
from flask import render_template
from flask_restful import Api,Resource,reqparse

from datahandle import intoMongo 

parser = reqparse.RequestParser()
app = Flask(__name__)



#接收prometheus的告警消息
@app.route('/promeData', methods=['POST'])
def promeData():
    data = request.data
    alertSource = request.remote_addr
    
    result = intoMongo(data, source = alertSource) 
    if result:
        return 'Insert success'
    else:
        return 'Insert failure'

#接收json格式的告警消息
@app.route('/fishData', methods=['POST'])
def fishData():
    data = request.data
    alertSource = request.remote_addr

    try:
        resDict = json.loads(data)
    except:    
        return 'Request object is not json format'
    else:
        if 'alertname' not in resDict or 'value' not in resDict:
            return 'Request object does not contain  key alertname or value'
        else:
            result = intoMongo(data, source = alertSource)
            if result:
                return 'Insert success'
            else:
                return 'Insert failure'


#接收告警消息
class alertData(Resource):
    #@pysnooper.snoop()
    def post(self):
        #parser.add_argument('name', type=str, location=['json','form'])
        parser.add_argument('source', type=str, default=socket.gethostname(), store_missing=True, location=['json'])
        parser.add_argument('alertname', type=str, dest='alertname', required=True, case_sensitive=True, trim=True, location=['json'], help='Missing argument "name"')
        parser.add_argument('value', type=int, ignore=True, required=True, action='store', case_sensitive=True, trim=True, location=['json'], help='Missing argument "value"')
        parser.add_argument('variable', type=isJson, default='{}', case_sensitive=True, trim=True, location=['json'], help='Argument "variable" type error')
        data = parser.parse_args()

        alertname = data['alertname']
        value = data['value']
        source = data['source']
        variable = str(data['variable'])

        SQL = 'INSERT INTO alertmsg(alertname, value, source, variable) values (\'{}\', {}, \'{}\', \'{}\');'.format(alertname, value, source, variable)
        #fidb.Insert(SQL)

        return data
    
    

class login(Resource):
    def get(self):
        form = LoginForm()
        return render_template('login.html', title="Sign In", form=form)

if __name__ == '__main__':
    main()