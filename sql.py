import os,sys
sys.path.append("D:/Users/CRT/PycharmProjects/untitled2")
import psycopg2
import time
import random
from web import config
class Server:
    def __init__(self):
        self.choice_server = config.config["yourserver"]
        if self.choice_server == "测试服":
            self.severname = "********"
            self.port = "********"
            self.username = "********"
            self.password = "********"
            self.database = 'test-********-web'
        if self.choice_server == "开发服":
            self.severname = "********"
            self.port = "********"
            self.username = "********"
            self.password = "********"
            self.database = '********'
        if self.choice_server == "********":
            self.severname = "********"
            self.port = "********"
            self.username = "********"
            self.password = "********"
            self.database = '********'
    def _GetConnect(self):
        self.conn = psycopg2.connect(host=self.severname,port=self.port,user=self.username,password=self.password,database=self.database)
        if not self.conn:
            print("连接失败!")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql,li=None):
        cur = self._GetConnect()
        cur.execute(sql)  # 执行查询语句
        result = cur.fetchall()  # fetchall()获取查询结果
        self.conn.close()
        #当li = 1的时候，将数据库查询的结果解析成列表(原先带有元组，解析会去掉元组)，这是为了应对查询单列的情况
        if li == 1:
            return [result[i][0] for i in range(len(result))]
        return result
    #ex:
    def get_timestamp(self):
        return int(time.time())
    def get_weekdays(self):
        return random.choice(['1','2','3','4','5','6','0'])

    def methods(self,your_meth1,):
        meth = list(filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)),
                            dir(self)))
        if your_meth1 in meth:
            return getattr(self,your_meth1)()
        else:
            return your_meth1