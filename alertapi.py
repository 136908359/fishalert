from flask_restful import Api,Resource,reqparse
import pysnooper,time,json,socket
import db,Config
import test

parser = reqparse.RequestParser()
fidb = db.fiDB()
config = Config.Config()


def isJson(data):
    # print(type(data))
    if isinstance(data, dict):
        json_data = json.dumps(data)
        return json_data
    else:
        # logging.error('')
        raise data + ': type is not dict'

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
        fidb.Insert(SQL)

        return data
    
    
#接收告警消息prometheus
class promeData(Resource):
    #@pysnooper.snoop()
    def post(self):
        data = parser.parse_args()
        print(data)
        return data

class login(Resource):
    def get(self):
        form = LoginForm()
        return render_template('login.html', title="Sign In", form=form)

if __name__ == '__main__':
    main()