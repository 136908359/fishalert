import pymysql,pymongo
import logging
import sys,traceback,pysnooper
from tools.parser import dbParser,baseParser,alertParser

class fiDB():

    database = dbParser.get('mysqlDatabase','fish')

    def __init__(self):
        self.host = dbParser.get('mysqlHost','127.0.0.1')
        self.port = dbParser.getint('mysqlPort', 3306)
        self.user = dbParser.get('mysqlUser','fish')
        self.password = dbParser.get('mysqlPassword')

    #连接数据库
    def conn(self):
        try:
            db = pymysql.connect(host=self.host,
                            port=self.port,
                            user=self.user,
                            password=self.password,
                            database=self.database,
                            charset='utf8')
        except pymysql.err.OperationalError as err:
            msg = self.host + ':' + str(self.port) + ',failed to connect database.'
            # logging.error(msg)
            return msg
        except:
            msg = traceback.print_exc(limit=10, file=sys.stdout)
            # logging.error(msg)
            return msg
        else:
            cursor = db.cursor(cursor = pymysql.cursors.DictCursor)
            return db, cursor

    #insert
    #@pysnooper.snoop()
    def Insert(self, SQL, database=database):
        db, cursor = self.conn()

        try:
            cursor.execute(SQL)
            db.commit()
        except pymysql.err.ProgrammingError:
            msg = 'You have an error in your SQL syntax: ' + SQL
            logging.error(msg)
            return msg
        except:
            msg = traceback.print_exc(limit=10, file=sys.stdout)
            logging.error(msg)
            return msg
        else:
            cursor.close()
            db.close()
            msg = 'Insert sucess: ' + SQL
            logging.debug(msg)

    #select
    def Select(self, SQL, database=database):
        db, cursor = self.conn()

        try:
            cursor.execute(SQL)
        except pymysql.err.ProgrammingError:
            msg = 'You have an error in your SQL syntax: ' + SQL
            logging.error(msg)
            return msg
        except:
            msg = traceback.print_exc(limit=10, file=sys.stdout)
            logging.error(msg)
            return msg
        else:
            data = cursor.fetchall()
            cursor.close()
            db.close()
            msg = 'Select sucess: ' + SQL
            logging.debug(msg)
            return data

        # insert
        # @pysnooper.snoop()
    #@pysnooper.snoop()
    def Update(self, SQL, database=database):
        db, cursor = self.conn()

        try:
            cursor.execute(SQL)
            db.commit()
        except pymysql.err.ProgrammingError:
            msg = 'You have an error in your SQL syntax: ' + SQL
            logging.error(msg)
            return msg
        except:
            msg = traceback.print_exc(limit=10, file=sys.stdout)
            logging.error(msg)
            return msg
        else:
            cursor.close()
            db.close()
            msg = 'Update sucess: ' + SQL
            logging.debug(msg)

        # insert
        # @pysnooper.snoop()

    def Delete(self, SQL, database=database):
        db, cursor = self.conn()

        try:
            cursor.execute(SQL)
            db.commit()
        except pymysql.err.ProgrammingError:
            msg = 'You have an error in your SQL syntax: ' + SQL
            logging.error(msg)
            return msg
        except:
            msg = traceback.print_exc(limit=10, file=sys.stdout)
            logging.error(msg)
            return msg
        else:
            cursor.close()
            db.close()
            msg = 'Delete sucess: ' + SQL
            logging.debug(msg)


class fiMongo(object):

    def __init__(self):
        self.host = dbParser.get('mongoHost', '127.0.0.1')
        self.port = dbParser.getint('mongoPort', 27017) 
    def conn(self):
        try:
            client = pymongo.MongoClient(host = self.host, port = self.port)
        except:
            msg = traceback.print_exc(limit=10, file=sys.stdout)
            logging.error(msg)
            return msg
        else:
            with client:
                db = client.fish
                return  db


if __name__ == '__main__':
    main()