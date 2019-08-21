import MySQLdb
from config import Config


class MySQLConn:

    def __init__(self):
        # self.db = MySQLdb.connect("localhost", "python", "python123", "pytestdb", charset='utf8'
        self.db = MySQLdb.connect(Config.MysqlConnectString['server'],
                                  Config.MysqlConnectString['username'],
                                  Config.MysqlConnectString['password'],
                                  Config.MysqlConnectString['database'],
                                  charset='utf8')

    def __del__(self):
        self.db.close()

    def execQuery(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    def execUID(self, sql):

        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
